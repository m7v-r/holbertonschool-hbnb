from app import db
from app.models.base import BaseModel
from sqlalchemy.orm import validates


class Amenity(BaseModel):
    __tablename__ = "amenities"

    name = db.Column(db.String(50), nullable=False)

    def __init__(self, name: str, **kwargs):
        super().__init__(**kwargs)
        self.name = name

    @validates("name")
    def validate_name(self, key, name):
        if not name or not isinstance(name, str) or not name.strip():
            raise ValueError("Amenity name must be a non-empty string.")
        if len(name.strip()) > 50:
            raise ValueError("Amenity name cannot exceed 50 characters.")
        return name.strip()

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "places": [place.id for place in self.places] if self.places else [],
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
