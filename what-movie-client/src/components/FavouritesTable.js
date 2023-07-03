const FavouritesTable = ({ favourites, onDelete }) => {
  return (
    <div className="table-responsive-sm">
      <table className="table">
        <thead>
          <tr>
            <th scope="col">Date</th>
            <th scope="col">Cinema ID</th>
            <th scope="col">Cinema Type</th>
            <th scope="col">Start Time</th>
            <th scope="col">End Time</th>
            <th scope="col">Film ID</th>
            <th scope="col">Delete</th>
          </tr>
        </thead>
        <tbody>
          {favourites.map((favourite) => (
            <tr key={favourite.id}>
              <td>{new Date(favourite.added_on).toLocaleDateString()}</td>
              <td>{favourite.cinema_id}</td>
              <td>{favourite.cinema_type}</td>
              <td>{favourite.start_time}</td>
              <td>{favourite.end_time}</td>
              <td>{favourite.film_id}</td>
              <td>
                <button onClick={() => onDelete(favourite.id)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default FavouritesTable;
