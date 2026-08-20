import os


class Config:
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "c810c978b272f2e519c72e38202df6bd4282e707bc36968c920f0f49861e6d1b",
    )
    JWT_SECRET_KEY = os.getenv(
        "JWT_SECRET_KEY",
        "c810c978b272f2e519c72e38202df6bd4282e707bc36968c920f0f49861e6d1b",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///development.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "mysql+pymysql://user:password@localhost/hbnb_prod"
    )


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
