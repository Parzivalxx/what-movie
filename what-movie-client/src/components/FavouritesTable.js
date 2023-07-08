import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faLocationDot, faTrashCan } from "@fortawesome/free-solid-svg-icons";
import { useNavigate } from "react-router-dom";

const FavouritesTable = ({ favourites, onDelete }) => {
  const navigate = useNavigate();

  const formatDate = (dateString) => {
    const date = new Date(dateString);

    // Extracting the date components
    const year = date.getFullYear();
    const month = date.getMonth(); // Month starts from 0, so add 1 to get the correct month
    const day = date.getDate();
    const months = [
      "January",
      "February",
      "March",
      "April",
      "May",
      "June",
      "July",
      "August",
      "September",
      "October",
      "November",
      "December",
    ];
    return `${day} ${months[month]} ${year}`;
  };

  return (
    <div className="table-responsive-sm">
      <table className="table align-middle">
        <thead>
          <tr>
            <th scope="col">Date</th>
            <th scope="col">Film</th>
            <th scope="col">Cinema</th>
            <th scope="col">Cinema Type</th>
            <th scope="col">Start Time</th>
            <th scope="col">End Time</th>
            <th scope="col">Delete</th>
          </tr>
        </thead>
        <tbody>
          {favourites.map((favourite) => (
            <tr key={favourite.id}>
              <td>{formatDate(favourite.added_on)}</td>
              <td>
                <button
                  type="button"
                  className="btn btn-light text-center"
                  onClick={() => navigate(`/movies/${favourite.film_id}`)}
                >
                  {favourite.movieDetail.film_name}
                </button>
              </td>
              <td>
                <a
                  href={`https://maps.google.com/maps?q=${favourite.cinemaDetail.lat},${favourite.cinemaDetail.lng}`}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  <button type="button" className="btn btn-light text-center">
                    {favourite.cinemaDetail.cinema_name}
                    <FontAwesomeIcon className="ps-2" icon={faLocationDot} />
                  </button>
                </a>
              </td>
              <td>{favourite.cinema_type}</td>
              <td>{favourite.start_time}</td>
              <td>{favourite.end_time}</td>
              <td>
                <button
                  className="btn btn-danger"
                  onClick={() => onDelete(favourite.id)}
                >
                  <FontAwesomeIcon icon={faTrashCan} />
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default FavouritesTable;
