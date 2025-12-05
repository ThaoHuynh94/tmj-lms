from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from .config import Config

# -------------------------------------------------------------
# Extensions
# -------------------------------------------------------------
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"  # where @login_required redirects


def create_app():
    """Application factory."""
    app = Flask(__name__)
    app.config.from_object(Config)

    # init extensions
    db.init_app(app)
    login_manager.init_app(app)

    # import models so User exists
    from .models import User

    # user loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # register blueprints
    from .auth.routes import auth_bp
    from .main.routes import main_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(main_bp)

    return app
