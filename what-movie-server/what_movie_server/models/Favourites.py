from what_movie_server.app import db


class Favourites(db.Model):
    """Favourites Model for storing user favourite showtimes"""

    __tablename__ = "favourites"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    film_id = db.Column(db.Integer, nullable=False)
    cinema_id = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.String(10), nullable=False)
    end_time = db.Column(db.String(10), nullable=False)
    cinema_type = db.Column(db.String(10), nullable=False)

    user = db.relationship(
        "User",
        backref=db.backref("favourites", lazy=True, cascade="all, delete-orphan"),
    )

    def __init__(
        self,
        user_id: int,
        film_id: int,
        cinema_id: int,
        start_time: str,
        end_time: str,
        cinema_type: str,
    ) -> None:
        self.user_id = user_id
        self.film_id = film_id
        self.cinema_id = cinema_id
        self.start_time = start_time
        self.end_time = end_time
        self.cinema_type = cinema_type
