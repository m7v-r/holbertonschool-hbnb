from app import db
from app.models.base import BaseModel
from sqlalchemy.orm import validates


class Review(BaseModel):
    __tablename__ = "reviews"

    text = db.Column(db.String(500), nullable=False)
    rating = db.Column(
        db.Integer,
        db.CheckConstraint("rating >= 1 AND rating <= 5", name="check_rating_range"),
        nullable=False,
    )

    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey("places.id"), nullable=False)

    def __init__(
        self,
        text: str,
        rating: int,
        user_id: str = None,
        place_id: str = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.text = text
        self.rating = rating
        if user_id:
            self.user_id = user_id
        if place_id:
            self.place_id = place_id

    @validates("text")
    def validate_text(self, key, text):
        if not text or not isinstance(text, str) or not text.strip():
            raise ValueError("Review text must be a non-empty string.")
        return text.strip()

    @validates("rating")
    def validate_rating(self, key, rating):
        try:
            val = int(rating)
            if val < 1 or val > 5:
                raise ValueError
            return val
        except (ValueError, TypeError):
            raise ValueError("Rating must be an integer between 1 and 5")

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "rating": self.rating,
            "user_id": self.user_id,
            "place_id": self.place_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
