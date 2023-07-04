import { useNavigate } from "react-router-dom";

const MoviesList = ({ movies }) => {
  const navigate = useNavigate();

  const handleButtonClick = (filmId) => {
    navigate(`/movies/${filmId}`);
  };

  return (
    <div className="container mt-5 ps-5 pe-5">
      <div className="card-deck row justify-content-center">
        {movies &&
          movies.map((movie) => (
            <div
              className="card col-md-3 col-lg-2 m-3 px-0"
              key={movie.film_id}
            >
              <img
                className="card-img-top"
                src={
                  movie.images.poster[1] &&
                  movie.images.poster[1].medium.film_image
                }
                alt={movie.film_name}
              />
              <div className="card-body">
                <h6 className="card-title">{movie.film_name}</h6>
              </div>
              <div className="card-footer">
                <button
                  type="button"
                  className="btn btn-primary btn-sm btn-block"
                  onClick={() => handleButtonClick(movie.film_id)}
                >
                  View more info
                </button>
              </div>
            </div>
          ))}
      </div>
    </div>
  );
};

export default MoviesList;
