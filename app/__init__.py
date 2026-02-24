import os

from dotenv import load_dotenv
from flask import Flask
from flask_minify import Minify

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    Minify(app=app, html=False, js=True, cssless=True, static=True)

    from app.models import init_db

    init_db()

    from app.error_handlers import bp as errors_bp
    from app.main_routes import bp as main_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(errors_bp)

    return app


__all__ = ["create_app"]
