import { Link } from "react-router-dom";

const MoviesList = ({ movies }) => {
  console.log(movies);
  return (
    <>
      <div>
        <h1>Movies Now Showing</h1>
      </div>

      <div className="card-deck">
        {movies.map((movie) => (
          <div className="card col-sm-5" key={movie.film_id}>
            <img
              className="card-img-top"
              src={movie.images.poster[1].medium.film_image}
              alt={movie.film_name}
            />
            <div className="card-body">
              <h5 className="card-title">{movie.film_name}</h5>
              <p className="card-text">{movie.synopsis_long}</p>
            </div>
            <div className="card-footer">
              <Link to={`/movies/${movie.film_id}`}>
                <button
                  type="button"
                  className="btn btn-primary btn-lg btn-block"
                >
                  View more info
                </button>
              </Link>
            </div>
          </div>
        ))}
        ;
      </div>
    </>
  );
};

export default MoviesList;
