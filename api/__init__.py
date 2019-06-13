__version__ = '19.06.02'

from typing import NamedTuple, Optional

from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from api import model


class Server(NamedTuple):
    flask_app: Flask
    flask_api: Api
    db: SQLAlchemy


server: Optional[Server] = None


def make_flask_server() -> Server:
    global server
    if server is not None:
        raise Exception('The server is already initialized')

    flask_app = Flask(__name__)
    flask_api = Api(flask_app)

    db = model.init_extensions(flask_app)

    server = Server(
        flask_app=flask_app,
        flask_api=flask_api,
        db=db
    )

    __import__('api.resource')

    return server
