import { useState, useEffect } from "react";
import { json } from "react-router-dom";

import { Accordion, Alert } from "react-bootstrap";
import FavouriteButton from "./FavouriteButton";

const Showtimes = ({ showtimes, user }) => {
  const [show, setShow] = useState(false);
  const [data, setData] = useState(null);
  const [favourites, setFavourites] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Run fetchData on initial page load
    fetchFavourites();
  }, [user]); // Empty dependency array ensures it runs only once on initial load

  const fetchFavourites = async () => {
    setIsLoading(true);
    try {
      if (!user) {
        setFavourites([]);
        setIsLoading(false);
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
        console.log(resData);
        setFavourites(resData.data);
        setIsLoading(false);
      }
    } catch (error) {
      console.error(error);
      return;
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
                    {data.message}
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
                                const matchingFavourite = favourites.find(
                                  (favourite) =>
                                    favourite.cinema_type === cinemaType &&
                                    favourite.cinema_id === cinema.cinema_id &&
                                    favourite.start_time === time.start_time &&
                                    favourite.end_time === time.end_time
                                );

                                const isFavourite = !!matchingFavourite;
                                const favouriteId = isFavourite
                                  ? matchingFavourite.id
                                  : null;
                                return (
                                  <FavouriteButton
                                    key={`${cinema.cinema_id}-${index}`}
                                    setShow={setShow}
                                    setData={setData}
                                    showtime={showtime}
                                    user={user}
                                    cinemaType={cinemaType}
                                    cinema={cinema}
                                    time={time}
                                    initialFavouriteId={favouriteId}
                                  />
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
