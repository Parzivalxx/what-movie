import { Suspense, useState, useEffect } from "react";
import { useRouteLoaderData, defer, Await } from "react-router-dom";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faUpRightFromSquare,
  faStar,
  faCalendar,
  faClock,
  faMasksTheater,
  faPerson,
  faVideo,
} from "@fortawesome/free-solid-svg-icons";

import Showtimes from "../components/Showtimes";
import "../css/MovieDetail.css";
import { useAuth } from "../hooks/Auth";

const MovieDetailPage = () => {
  const { showtimes } = useRouteLoaderData("movie-showtimes");
  const { user } = useAuth();
  const [movieDetails, setMovieDetails] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const film_id = window.location.pathname.split("/").pop();

  useEffect(() => {
    // Run fetchData on initial page load
    fetchDetails();
  }, [user]); // Empty dependency array ensures it runs only once on initial load

  const fetchDetails = async () => {
    setIsLoading(true);
    try {
      const params = {
        film_id: film_id,
      };
      const queryString = new URLSearchParams(params).toString();
      const response = await fetch(
        `http://localhost:5000/movies/details?${queryString}`,
        {
          method: "GET",
        }
      );
      if (!response.ok) {
        throw JSON.stringify({
          message: "Could not fetch details",
          status: 500,
        });
      } else {
        const resData = await response.json();
        if (resData.status === "fail") {
          console.error(resData.message);
          return;
        }
        setMovieDetails(resData.data);
        setIsLoading(false);
      }
    } catch (error) {
      console.error(error);
      return;
    }
  };

  const renderStarRating = (numStars) => {
    const stars = [];
    for (let i = 0; i < numStars; i++) {
      stars.push(
        <FontAwesomeIcon key={i} icon={faStar} style={{ color: "gold" }} />
      );
    }
    return stars;
  };

  const formatDuration = (duration) => {
    if (duration !== null) {
      const hours = Math.floor(duration / 60);
      const minutes = duration % 60;

      let formattedDuration = "";

      if (hours > 0) {
        formattedDuration += `${hours}h `;
      }

      if (minutes > 0) {
        formattedDuration += `${minutes}m`;
      }

      return formattedDuration;
    }

    return "";
  };

  const formatArray = (arr, field) => {
    if (arr && Array.isArray(arr)) {
      return arr.map((elem) => elem[field]).join(", ");
    }

    return "";
  };

  return (
    <>
      {isLoading ? (
        <div className="text-center mt-5">Loading...</div>
      ) : (
        <div className="container col-lg-8 justify-content-center">
          <div className="container">
            <section id="about" className="about">
              <div className="row pt-5">
                <div className="pt-lg-0">
                  <h3>{movieDetails.film_name}</h3>
                  <br />
                  <img
                    src={
                      movieDetails.images &&
                      movieDetails.images.poster &&
                      movieDetails.images.poster[1] &&
                      movieDetails.images.poster[1].medium.film_image
                    }
                    className="float-end detail-img imgshadow ps-5 pb-5"
                    alt={movieDetails.film_name}
                  />
                  <p className="pb-3 details">{movieDetails.synopsis_long}</p>
                  <p className="details">
                    <b className="pe-2">Rating:</b>
                    {movieDetails.review_stars
                      ? renderStarRating(movieDetails.review_stars)
                      : "No rating found"}
                  </p>
                  <p className="details">
                    <b className="pe-2">Release date:</b>
                    <FontAwesomeIcon className="pe-2" icon={faCalendar} />
                    {movieDetails.release_dates &&
                      movieDetails.release_dates[0] &&
                      movieDetails.release_dates[0].release_date}
                  </p>
                  {movieDetails.age_rating && movieDetails.age_rating[0] && (
                    <p className="details">
                      <b className="pe-2">Age rating:</b>
                      <img
                        src={movieDetails.age_rating[0].age_rating_image}
                        alt={movieDetails.age_rating[0].rating}
                      />
                    </p>
                  )}
                  <p className="details">
                    <b className="pe-2">Duration:</b>
                    <FontAwesomeIcon className="pe-2" icon={faClock} />
                    {formatDuration(movieDetails.duration_mins)}
                  </p>
                  <p className="details">
                    <b className="pe-2">Genre:</b>
                    <FontAwesomeIcon className="pe-2" icon={faMasksTheater} />
                    {formatArray(movieDetails.genres, "genre_name")}
                  </p>
                  <p className="details">
                    <b className="pe-2">Directors:</b>
                    <FontAwesomeIcon className="pe-2" icon={faVideo} />
                    {formatArray(movieDetails.directors, "director_name")}
                  </p>
                  <p className="details">
                    <b className="pe-2">Cast:</b>
                    <FontAwesomeIcon className="pe-2" icon={faPerson} />
                    {formatArray(movieDetails.cast, "cast_name")}
                  </p>
                  <a
                    href={`https://www.imdb.com/title/${movieDetails.imdb_title_id}`}
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    <button className="my-5 pt-2 btn btn-primary btn-sm btn-block border w-100 text-center">
                      <h5>
                        View more info on IMDB
                        <FontAwesomeIcon
                          className="ps-2"
                          icon={faUpRightFromSquare}
                        />
                      </h5>
                    </button>
                  </a>
                </div>
              </div>
            </section>
          </div>
          {movieDetails.trailers &&
            movieDetails.trailers.high &&
            movieDetails.trailers.high[0] && (
              <div className="container mb-5 vid">
                <video controls className="w-100">
                  <source
                    src={movieDetails.trailers.high[0].film_trailer}
                    type="video/mp4"
                  />
                  Your browser does not support video tag
                </video>
              </div>
            )}
          <hr />
          <div className="my-5 text-center">
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
      )}
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
    throw JSON.stringify({
      message: "Could not fetch details for selected movie.",
      status: 500,
    });
  } else {
    if (response.status === 204) {
      return [];
    }
    const resData = await response.json();
    if (resData.status === "fail") {
      console.error(resData.message);
      return;
    }
    return resData.data.cinemas;
  }
};

export const loader = async ({ params }) => {
  const { movieId } = params;

  return defer({
    showtimes: await loadShowtimes(movieId),
  });
};
