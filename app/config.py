import os
BASE_DIR = os.path.dirname(__file__)

class Config:
    # Team-defined placeholder secret key (safe for development)
    SECRET_KEY = os.environ.get("SECRET_KEY", "tmj-team-secret")

    # SQLite database URI (local development)
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///" + os.path.join(BASE_DIR, "app.db")
    )

    # Disable modification tracking to save resources
    SQLALCHEMY_TRACK_MODIFICATIONS = False

