import { useEffect, useState } from "react";

import { useAuth } from "../hooks/Auth";
import FavouritesTable from "../components/FavouritesTable";

const FavouritesPage = () => {
  const [isLoading, setIsLoading] = useState(true);
  const [favourites, setFavourites] = useState([]);
  const { user } = useAuth();

  useEffect(() => {
    // Run fetchData on initial page load
    fetchFavourites(user);
  }, [user]); // Empty dependency array ensures it runs only once on initial load

  const fetchFavourites = async (user) => {
    setIsLoading(true);
    try {
      if (!user) {
        return;
      }
      const params = {
        user_id: user.user_id,
      };
      const queryString = new URLSearchParams(params).toString();
      const response = await fetch(
        `http://localhost:5000/favourites?${queryString}`,
        {
          method: "GET",
        }
      );
      if (!response.ok) {
        throw JSON.stringify({
          message: "Could not fetch favourites",
          status: 500,
        });
      } else {
        const resData = await response.json();
        if (resData.status === "fail") {
          console.error(resData.message);
          return;
        }
        const favouritesWithDetails = await Promise.all(
          resData.data.map(async (favourite) => {
            const movieDetails = await fetchMovieDetails(favourite.film_id);
            const cinemaDetails = await fetchCinemaDetails(favourite.cinema_id);
            return {
              ...favourite,
              movieDetail: movieDetails,
              cinemaDetail: cinemaDetails,
            };
          })
        );
        favouritesWithDetails.sort((a, b) => {
          const dateA = new Date(a.added_on);
          const dateB = new Date(b.added_on);
          if (dateB.toLocaleDateString() !== dateA.toLocaleDateString()) {
            return dateB - dateA;
          }
          if (b.film_id !== a.film_id) {
            return b.film_id - a.film_id;
          }
          if (b.start_time !== a.start_time) {
            return a.start_time.localeCompare(b.start_time);
          }
          return a.end_time.localeCompare(b.end_time);
        });
        setFavourites(favouritesWithDetails);
        setIsLoading(false);
      }
    } catch (error) {
      console.error(error);
      return;
    }
  };

  const fetchMovieDetails = async (movieId) => {
    const params = {
      film_id: movieId,
    };
    const queryString = new URLSearchParams(params).toString();
    const response = await fetch(
      `http://localhost:5000/movies/details?${queryString}`
    );
    if (!response.ok) {
      throw JSON.stringify({
        message: "Could not fetch movie details",
        status: 500,
      });
    } else {
      const resData = await response.json();
      if (resData.status === "fail") {
        console.error(resData.message);
        return;
      }
      return resData.data;
    }
  };

  const fetchCinemaDetails = async (cinemaId) => {
    const params = {
      cinema_id: cinemaId,
    };
    const queryString = new URLSearchParams(params).toString();
    const response = await fetch(
      `http://localhost:5000/cinemas/details?${queryString}`
    );
    if (!response.ok) {
      throw JSON.stringify({
        message: "Could not fetch cinema details",
        status: 500,
      });
    } else {
      const resData = await response.json();
      if (resData.status === "fail") {
        console.error(resData.message);
        return;
      }
      return resData.data;
    }
  };

  const handleDelete = (id) => {
    // Perform the delete operation and update the favourites state
    // Here's an example assuming you are making an API request to delete the favourite
    deleteFavourite(id)
      .then(() => {
        // Remove the deleted favourite from the state
        setFavourites((prevFavourites) =>
          prevFavourites.filter((favourite) => favourite.id !== id)
        );
      })
      .catch((error) => {
        console.error("Error deleting favourite:", error);
      });
  };

  const deleteFavourite = (id) => {
    // Implement your API delete request logic here
    // Return a Promise that resolves when the delete operation is successful
    return fetch(`http://localhost:5000/favourites/${id}`, {
      method: "DELETE",
    }).then((response) => {
      if (!response.ok) {
        throw new Error("Failed to delete favourite");
      }
    });
  };

  return (
    <div className="mt-5 text-center">
      <h4>My Favourites</h4>
      <div className="my-5 container col-lg-10 justify-content-center">
        {isLoading ? (
          <div className="text-center mt-5">Loading...</div>
        ) : (
          <div>
            <FavouritesTable favourites={favourites} onDelete={handleDelete} />
          </div>
        )}
      </div>
    </div>
  );
};

export default FavouritesPage;
