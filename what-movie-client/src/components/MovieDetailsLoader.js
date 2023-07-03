import { json, useLocation } from "react-router-dom";

import { useAuth } from "../hooks/Auth";

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

const fetchFavourites = async (userId) => {
  const params = {
    user_id: userId,
  };
  const queryString = new URLSearchParams(params).toString();
  const response = await fetch(
    `http://localhost:5000/favourites?${queryString}`,
    {
      method: "GET",
    }
  );
  if (!response.ok) {
    throw json(
      { message: "Could not fetch favourites for user." },
      {
        status: 500,
      }
    );
  } else {
    if (response.status === 204) {
      return [];
    }
    const resData = await response.json();
    console.log(resData.data);
    return resData.data;
  }
};

const MovieDetailsLoader = async () => {
  const { user } = useAuth();
  const location = useLocation();
  const params = new URLSearchParams(location.search);
  const movieId = params.get("movieId");

  const favourites = user ? await fetchFavourites(user.id) : [];
  const showtimes = await loadShowtimes(movieId);

  return { favourites, showtimes };
};

export default MovieDetailsLoader;
