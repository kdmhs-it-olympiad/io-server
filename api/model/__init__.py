from flask_sqlalchemy import SQLAlchemy

from config import config


db = SQLAlchemy()


def init_extensions(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}/{}?charset=utf8'.format(
                                            config.DB_USER, config.DB_PASSWORD, config.DB_ADDRESS, config.DB_NAME)
    db.init_app(app)
    return db


__import__('api.model.calender')
