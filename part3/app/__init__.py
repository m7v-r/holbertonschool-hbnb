from flask import Flask
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()


def create_app(config_name="default"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    CORS(app, resources={
        r"/api/*": {
            "origins": "*"
        }
    })

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    from app.api.v1.auth import auth_bp

    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")

    from app.api.v1 import api_v1

    app.register_blueprint(api_v1, url_prefix="/api/v1")

    with app.app_context():
        from app.models.user import User
        from app.models.place import Place
        from app.models.review import Review
        from app.models.amenity import Amenity

        db.create_all()

    return app
