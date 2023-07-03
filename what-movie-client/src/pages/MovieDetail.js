import { Suspense } from "react";
import {
  useRouteLoaderData,
  json,
  defer,
  Await,
  useLocation,
} from "react-router-dom";

import Showtimes from "../components/Showtimes";
import "../css/MovieDetail.css";
import { useAuth } from "../hooks/Auth";

const MovieDetailPage = () => {
  const { showtimes } = useRouteLoaderData("movie-showtimes");
  const { user } = useAuth();
  const location = useLocation();
  const {
    ageRating,
    filmName,
    filmTrailer,
    poster,
    titleId,
    releaseDate,
    synopsisLong,
  } = location.state;

  return (
    <>
      <div className="container col-lg-8 justify-content-center">
        <div className="container">
          <section id="about" className="about">
            <div className="row pt-5">
              <div className="pt-lg-0">
                <h3>{filmName}</h3>
                <br />
                <img
                  src={poster}
                  className="float-end imgshadow ps-5 pb-5"
                  alt={filmName}
                  style={{ width: "220px", height: "300px" }}
                />
                <p>{synopsisLong}</p>
                <p>
                  <b>Release date: </b>
                  {releaseDate}
                </p>
                {ageRating && ageRating[0] && (
                  <div>
                    <div>
                      <b>Age rating: </b>
                      {ageRating[0].rating}
                      <img
                        src={ageRating[0].age_rating_image}
                        alt={ageRating[0].rating}
                      />
                    </div>
                    {ageRating[0].age_advisory && (
                      <p>
                        <b>Age advisory: </b>
                        {ageRating[0].age_advisory}
                      </p>
                    )}
                  </div>
                )}
                <p>
                  <b>Find out more on IMDB: </b>
                  <a
                    href={`https://www.imdb.com/title/${titleId}`}
                    target="_blank"
                    rel="noreferrer"
                  >
                    Link
                  </a>
                </p>
              </div>
            </div>
          </section>
        </div>
        {filmTrailer && (
          <div className="container mt-5 vid">
            <video controls className="w-100">
              <source src={filmTrailer} type="video/mp4" />
              Your browser does not support video tag
            </video>
          </div>
        )}
        <div className="mt-5 text-center">
          <h4>Showtimes today</h4>
          <Suspense
            fallback={
              <p style={{ textAlign: "center", marginTop: 15 }}>Loading...</p>
            }
          >
            <Await resolve={showtimes}>
              {(loadedShowtimes) => (
                <Showtimes showtimes={loadedShowtimes} user={user} />
              )}
            </Await>
          </Suspense>
        </div>
      </div>
    </>
  );
};

export default MovieDetailPage;

const loadShowtimes = async (id) => {
  const currentDate = new Date();
  const year = currentDate.getFullYear();
  const month = String(currentDate.getMonth() + 1).padStart(2, "0"); // Months are zero-based
  const day = String(currentDate.getDate()).padStart(2, "0");
  const params = {
    film_id: id,
    date: `${year}-${month}-${day}`,
    n: 10,
  };
  const queryString = new URLSearchParams(params).toString();
  // console.log(id);
  const response = await fetch(
    `http://localhost:5000/movies/showtimes?${queryString}`,
    {
      method: "GET",
    }
  );

  if (!response.ok) {
    throw json(
      { message: "Could not fetch details for selected movie." },
      {
        status: 500,
      }
    );
  } else {
    if (response.status === 204) {
      return [];
    }
    const resData = await response.json();
    console.log(resData.data.cinemas);
    return resData.data.cinemas;
  }
};

export const loader = async ({ params }) => {
  const { movieId } = params;

  return defer({
    showtimes: await loadShowtimes(movieId),
  });
};
