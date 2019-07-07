from sqlalchemy.dialects.mysql import ENUM

from api.model import db


class CalenderModel(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)

    context = db.Column(db.String(32), nullable=True)

    begin = db.Column(db.DateTime, nullable=False)

    end = db.Column(db.DateTime, nullable=False)

    status = db.Column(db.String(64), nullable=False)

    visable = db.Column(db.Boolean, nullable=False)
