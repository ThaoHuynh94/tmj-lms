# tests/test_forms.py

import os
import sys

# Make sure Python can find the "app" package (project root)
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app import create_app
from app.forms import LoginForm


def create_test_app():
    app = create_app()
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False  # disable CSRF for tests
    return app


def test_login_form_valid_data():
    app = create_test_app()
    with app.test_request_context("/auth/login", method="POST"):
        # Change "username" to whatever your LoginForm field is called
        form = LoginForm(username="student1", password="secret123")
        assert form.validate() is True


def test_login_form_missing_username():
    app = create_test_app()
    with app.test_request_context("/auth/login", method="POST"):
        form = LoginForm(username="", password="secret123")
        assert form.validate() is False

