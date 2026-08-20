import re
from app import db, bcrypt
from app.models.base import BaseModel
from sqlalchemy.orm import validates


class User(BaseModel):
    __tablename__ = "users"

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    places = db.relationship(
        "Place", backref="owner", lazy=True, cascade="all, delete-orphan"
    )
    reviews = db.relationship(
        "Review", backref="author", lazy=True, cascade="all, delete-orphan"
    )

    def __init__(
        self, first_name, last_name, email, password, is_admin=False, **kwargs
    ):
        super().__init__(**kwargs)
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin

        if password:
            self.password_hash = self.hash_password(password)

    @validates("first_name")
    def validate_first_name(self, key, value):
        if not value or not isinstance(value, str) or not value.strip():
            raise ValueError("First name is required and must be a non-empty string.")
        if len(value.strip()) > 50:
            raise ValueError("First name cannot exceed 50 characters.")
        return value.strip()

    @validates("last_name")
    def validate_last_name(self, key, value):
        if not value or not isinstance(value, str) or not value.strip():
            raise ValueError("Last name is required and must be a non-empty string.")
        if len(value.strip()) > 50:
            raise ValueError("Last name cannot exceed 50 characters.")
        return value.strip()

    @validates("email")
    def validate_email(self, key, value):
        if not value or not isinstance(value, str):
            raise ValueError("Email is required.")
        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_regex, value.strip()):
            raise ValueError("Invalid email format.")
        return value.strip()

    def hash_password(self, password):
        """Hashes plain text password or returns hash if already hashed."""
        if not password or not isinstance(password, str) or not password.strip():
            raise ValueError("Password is required and must be a non-empty string.")
        if password.startswith("$2b$"):
            return password
        return bcrypt.generate_password_hash(password).decode("utf-8")

    def verify_password(self, password):
        """Verify plain text password against stored hash."""
        return bcrypt.check_password_hash(self.password_hash, password)

    def to_dict(self):
        """Serialize User object to dictionary."""
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_admin": self.is_admin,
            "places": [place.id for place in self.places] if self.places else [],
            "reviews": [review.id for review in self.reviews] if self.reviews else [],
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
