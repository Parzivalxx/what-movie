import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { Accordion, Button, Alert } from "react-bootstrap";

const Showtimes = ({ showtimes, user }) => {
  const [show, setShow] = useState(false);
  const [data, setData] = useState(null);
  const navigate = useNavigate();

  const handleAddToFavourites = async (
    cinemaType,
    user,
    showtime,
    cinema,
    time
  ) => {
    if (!user) {
      return navigate("/auth?mode=login");
    }
    const payload = {
      user_id: parseInt(user.user_id),
      film_id: parseInt(showtime.film_id),
      cinema_id: parseInt(cinema.cinema_id),
      start_time: time.start_time,
      end_time: time.end_time,
      cinema_type: cinemaType,
    };

    try {
      const response = await fetch("http://localhost:5000/favourites", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });
      if (response.status === 422 || response.status === 401) {
        return response;
      }

      const resData = await response.json();
      console.log(resData);

      if (resData.status === "fail") {
        setShow(true);
        setData(resData);
        return;
      }
      setShow(true);
      setData(resData);
      return;
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="my-5">
      {showtimes && showtimes.length === 0 ? (
        <h5 className="text-center">No showtimes available</h5>
      ) : (
        <>
          {show &&
            ((data.status === "success" && (
              <Alert
                key="success"
                onClose={() => setShow(false)}
                dismissible
                variant="success"
              >
                Favourite added successfully
              </Alert>
            )) ||
              (data.status === "fail" && (
                <Alert
                  key="danger"
                  onClose={() => setShow(false)}
                  dismissible
                  variant="danger"
                >
                  {data.message}
                </Alert>
              )))}
          <Accordion defaultActiveKey={showtimes[0].cinema_id.toString()}>
            {showtimes.map((cinema) => (
              <Accordion.Item
                key={cinema.cinema_id.toString()}
                eventKey={cinema.cinema_id.toString()}
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
                  {Object.entries(cinema.showings).map(
                    ([cinemaType, showtime]) => (
                      <div key={cinemaType}>
                        <h5 className="py-2">{cinemaType}</h5>
                        <div
                          className="d-flex flex-wrap justify-content-center"
                          key={cinemaType}
                        >
                          {showtime.times.map((time, index) => (
                            <Button
                              key={index}
                              onClick={() =>
                                handleAddToFavourites(
                                  cinemaType,
                                  user,
                                  showtime,
                                  cinema,
                                  time
                                )
                              }
                              className="mx-2 mb-2"
                              variant="primary"
                            >
                              {time.start_time} - {time.end_time}
                            </Button>
                          ))}
                        </div>
                      </div>
                    )
                  )}
                </Accordion.Body>
              </Accordion.Item>
            ))}
          </Accordion>
        </>
      )}
    </div>
  );
};

export default Showtimes;
