from flask import Flask
from app.config import Config
from app.database import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from app.models import Categoria, Plato, Reserva, Mensaje
    from app.routes.public import public_bp

    app.register_blueprint(public_bp)

    return app