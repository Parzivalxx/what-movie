import { Link } from "react-router-dom";

const MoviesList = ({ movies }) => {
  return (
    <div className="container mt-5 ps-5 pe-5">
      <div className="card-deck row">
        {movies &&
          movies.map((movie) => (
            <div className="card col-sm-2 m-3" key={movie.film_id}>
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
                <Link to={`/movies/${movie.film_id}`}>
                  <button
                    type="button"
                    className="btn btn-primary btn-sm btn-block"
                  >
                    View more info
                  </button>
                </Link>
              </div>
            </div>
          ))}
      </div>
    </div>
  );
};

export default MoviesList;
