from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    """User model for login management (non-functional for M1)."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    email = db.Column(db.String(120), unique=True, index=True)
    password_hash = db.Column(db.String(128))  # placeholder only for M1

    def __repr__(self):
        return f"<User {self.username}>"

class Course(db.Model):
    """Simple course model stub (domain model example)."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f"<Course {self.title}>"

