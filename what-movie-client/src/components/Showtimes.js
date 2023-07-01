// import { Link, useRouteLoaderData, useSubmit } from "react-router-dom";
import { Accordion, Button } from "react-bootstrap";

const Showtimes = ({ showtimes }) => {
  // const token = useRouteLoaderData("root");
  // const submit = useSubmit();

  // const addFavouriteHandler = () => {
  //   submit(null, { method: "delete" });
  // };
  const handleAddToFavourites = (timing) => {
    console.log("lol");
  };

  return (
    <div className="my-5">
      {showtimes && showtimes.length === 0 ? (
        <h5 className="text-center">No showtimes available</h5>
      ) : (
        <Accordion
          defaultActiveKey={`dropdown-${showtimes[0].cinema_id.toString()}`}
        >
          {showtimes.map((cinema) => (
            <Accordion.Item
              eventKey={`dropdown-${cinema.cinema_id.toString()}`}
            >
              <Accordion.Header>
                <span className="d-inline-block col-5 text-start">
                  {cinema.cinema_name}
                </span>
                <span className="d-inline-block col-5 text-start">
                  Distance: {(cinema.distance * 1.609344).toFixed(1)}km
                </span>
              </Accordion.Header>
              <Accordion.Body>
                {Object.entries(cinema.showings).map(([version, showtime]) => (
                  <div key={version}>
                    <h5 className="py-2">{version}</h5>
                    <div className="d-flex flex-wrap justify-content-center">
                      {showtime.times.map((time, index) => (
                        <Button
                          key={index}
                          onClick={() => handleAddToFavourites(time)}
                          className="mx-2 mb-2"
                          variant="primary"
                        >
                          {time.start_time} - {time.end_time}
                        </Button>
                      ))}
                    </div>
                  </div>
                ))}
              </Accordion.Body>
            </Accordion.Item>
          ))}
        </Accordion>
      )}
    </div>
  );
};

export default Showtimes;
