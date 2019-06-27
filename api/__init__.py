__version__ = '19.06.02'

from typing import NamedTuple, Optional

from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

from api import model
from config import config


class Server(NamedTuple):
    flask_app: Flask
    flask_api: Api
    jwt: JWTManager
    db: SQLAlchemy


server: Optional[Server] = None


def make_flask_server() -> Server:
    global server
    if server is not None:
        raise Exception('The server is already initialized')

    flask_app = Flask(__name__)
    flask_api = Api(flask_app)

    flask_app.config['JWT_SECRET_KEY'] = config.JWT_SECRET_KEY
    jwt = JWTManager(flask_app)

    db = model.init_extensions(flask_app)

    CORS(flask_app)

    server = Server(
        flask_app=flask_app,
        flask_api=flask_api,
        jwt=jwt,
        db=db
    )

    __import__('api.resource')

    return server