import { Suspense } from "react";
import { useLoaderData, json, defer, Await } from "react-router-dom";

import MoviesList from "../components/MoviesList";

const NowShowingMoviesPage = () => {
  const { movies } = useLoaderData();

  return (
    <Suspense fallback={<p style={{ textAlign: "center" }}>Loading...</p>}>
      <Await resolve={movies}>
        {(loadedMovies) => <MoviesList movies={loadedMovies} />}
      </Await>
    </Suspense>
  );
};

export default NowShowingMoviesPage;

const loadNowShowingMovies = async () => {
  const response = await fetch("http://localhost:5000/movies/nowshowing", {
    method: "GET",
    // body: JSON.stringify({ n: 10 }),
  });

  if (!response.ok) {
    throw json(
      { message: "Could not fetch now showing movies." },
      {
        status: 500,
      }
    );
  } else {
    const resData = await response.json();
    console.log(resData.data.films);
    return resData.data.films;
  }
};

export const loader = () => {
  return defer({
    movies: loadNowShowingMovies(),
  });
};
