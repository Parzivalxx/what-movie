import { useState, useEffect } from "react";
import { json, useNavigate } from "react-router-dom";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faHeart as faHeartSolid } from "@fortawesome/free-solid-svg-icons";
import { faHeart as faHeartRegular } from "@fortawesome/free-regular-svg-icons";

import { Accordion, Button, Alert } from "react-bootstrap";

const Showtimes = ({ showtimes, user }) => {
  const [show, setShow] = useState(false);
  const [data, setData] = useState(null);
  const [favourites, setFavourites] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  const navigate = useNavigate();

  useEffect(() => {
    // Run fetchData on initial page load
    fetchFavourites();
  }, [user]); // Empty dependency array ensures it runs only once on initial load

  const fetchFavourites = async () => {
    setIsLoading(true);
    try {
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
        console.log(resData);
        setFavourites(resData.data);
        setIsLoading(false);
      }
    } catch (error) {
      console.error(error);
      return;
    }
  };

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
      {isLoading ? (
        <div style={{ textAlign: "center", marginTop: 15 }}>Loading...</div>
      ) : (
        <>
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
                              {showtime.times.map((time, index) => {
                                // Check if the showtime is a favorite
                                const isFavourite = favourites.some(
                                  (favourite) =>
                                    favourite.cinema_type === cinemaType &&
                                    favourite.cinema_id === cinema.cinema_id &&
                                    favourite.start_time === time.start_time &&
                                    favourite.end_time === time.end_time
                                );

                                return (
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
                                    variant="light"
                                  >
                                    {time.start_time} - {time.end_time}
                                    <FontAwesomeIcon
                                      className="ms-2"
                                      icon={
                                        isFavourite
                                          ? faHeartSolid
                                          : faHeartRegular
                                      }
                                      style={{
                                        color: "#ff0000",
                                      }}
                                    />
                                  </Button>
                                );
                              })}
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
        </>
      )}
    </div>
  );
};

export default Showtimes;
