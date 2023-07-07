import { useState, useEffect } from "react";

import "../css/MoviesNavigation.css";
import MoviesList from "../components/MoviesList";

const MoviesPage = () => {
  const [activeButton, setActiveButton] = useState("nowshowing");
  const [moviesData, setMoviesData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  const handleButtonClick = (buttonId) => {
    setActiveButton(buttonId);
    loadMovies(buttonId);
  };

  useEffect(() => {
    // Run fetchData on initial page load
    loadMovies(activeButton);
  }, [activeButton]); // Empty dependency array ensures it runs only once on initial load

  const loadMovies = async (buttonId) => {
    setIsLoading(true);
    try {
      const response = await fetch(`http://localhost:5000/movies/${buttonId}`, {
        method: "GET",
        // body: JSON.stringify({ n: 10 }),
      });
      if (!response.ok) {
        throw JSON.stringify({
          message: "Could not fetch now showing movies.",
          status: 500,
        });
      } else {
        const resData = await response.json();
        if (resData.status === "fail") {
          console.error(resData.message);
          return;
        }
        setMoviesData(resData.data.films);
        setIsLoading(false);
      }
    } catch (error) {
      console.error(error);
      return;
    }
  };

  return (
    <>
      <ul className="mt-4 nav nav-pills justify-content-center">
        <li className="nav-item">
          <button
            id="nowshowing"
            className={`btn nav-btn ${
              activeButton === "nowshowing" ? "active" : ""
            }`}
            onClick={() => handleButtonClick("nowshowing")}
          >
            Now Showing
          </button>
        </li>
        <li className="nav-item">
          <button
            id="comingsoon"
            className={`btn nav-btn ${
              activeButton === "comingsoon" ? "active" : ""
            }`}
            onClick={() => handleButtonClick("comingsoon")}
          >
            Coming Soon
          </button>
        </li>
      </ul>
      {isLoading ? (
        <div className="text-center mt-5">Loading...</div>
      ) : (
        <MoviesList movies={moviesData} />
      )}
    </>
  );
};

export default MoviesPage;
