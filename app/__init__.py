from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    #stub loader for  Flask-Login in M1
    from .models import User  
    @login_manager.user_loader
    def load_user(user_id):
        # M1: no real auth; keep everyone anonymous
        return None

    from .auth.routes import auth_bp
    from .main.routes import main_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(main_bp)

    return app
