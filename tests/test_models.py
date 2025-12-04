# tests/test_models.py

import os
import sys

# Make sure Python can find the 'app' package
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app import create_app, db
from app.models import User, Course


def create_test_app():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    return app


def test_create_user():
    app = create_test_app()
    with app.app_context():
        # 👇 ensure a clean DB each time
        db.drop_all()
        db.create_all()

        user = User(username="unit_test_user")
        db.session.add(user)
        db.session.commit()

        saved = User.query.filter_by(username="unit_test_user").first()
        assert saved is not None
        assert saved.username == "unit_test_user"


def test_create_course():
    app = create_test_app()
    with app.app_context():
        # 👇 also start clean here
        db.drop_all()
        db.create_all()

        # Adjust 'title' → 'name' if your model uses a different field
        course = Course(title="Intro to Python")
        db.session.add(course)
        db.session.commit()

        saved = Course.query.filter_by(title="Intro to Python").first()
        assert saved is not None
        assert saved.title == "Intro to Python"

