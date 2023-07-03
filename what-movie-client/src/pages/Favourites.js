import { json, useEffect, useState } from "react";

import { useAuth } from "../hooks/Auth";
import FavouritesTable from "../components/FavouritesTable";

const FavouritesPage = () => {
  const [isLoading, setIsLoading] = useState(true);
  const [favourites, setFavourites] = useState([]);
  const { user } = useAuth();
  console.log(user);

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
        throw json(
          { message: "Could not fetch favourites" },
          {
            status: 500,
          }
        );
      } else {
        const resData = await response.json();
        console.log(resData.data);
        setFavourites(resData.data);
        setIsLoading(false);
      }
    } catch (error) {
      console.error(error);
      return;
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
          <div style={{ textAlign: "center", marginTop: 15 }}>Loading...</div>
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
