import { useNavigate } from "react-router-dom";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faHeart as faHeartSolid } from "@fortawesome/free-solid-svg-icons";
import { faHeart as faHeartRegular } from "@fortawesome/free-regular-svg-icons";
import { useState } from "react";
import { Button } from "react-bootstrap";

const FavouriteButton = ({
  buttonKey,
  setShow,
  setData,
  showtime,
  user,
  cinemaType,
  cinema,
  time,
  initialFavouriteId,
}) => {
  const navigate = useNavigate();
  const [favouriteId, setFavouriteId] = useState(initialFavouriteId);

  const handleButtonClick = async (
    setShow,
    setData,
    cinemaType,
    user,
    showtime,
    cinema,
    time,
    favouriteId
  ) => {
    if (!user) {
      return navigate("/auth?mode=login");
    }

    if (favouriteId) {
      try {
        const response = await fetch(
          `http://localhost:5000/favourites/${favouriteId}`,
          {
            method: "DELETE",
          }
        );
        if (response.status === 422 || response.status === 401) {
          return response;
        }

        const resData = await response.json();

        if (resData.status === "fail") {
          setShow(true);
          setData(resData);
          return;
        }
        setFavouriteId(null);
        return;
      } catch (error) {
        console.error(error);
        return;
      }
    } else {
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

        if (resData.status === "fail") {
          setShow(true);
          setData(resData);
          return;
        }
        setFavouriteId(resData.message.split(" ")[1]);
        return;
      } catch (error) {
        console.error(error);
      }
    }
  };

  return (
    <Button
      key={buttonKey}
      onClick={() =>
        handleButtonClick(
          setShow,
          setData,
          cinemaType,
          user,
          showtime,
          cinema,
          time,
          favouriteId
        )
      }
      className="mx-2 mb-2"
      variant="light"
      favourite-id={favouriteId}
    >
      {time.start_time} - {time.end_time}
      <FontAwesomeIcon
        className="ms-2"
        icon={favouriteId ? faHeartSolid : faHeartRegular}
        style={{
          color: "#ff0000",
        }}
      />
    </Button>
  );
};

export default FavouriteButton;
