from sqlalchemy.schema import Column

from api.model import db


class CalenderModel(db.Model):
    id = Column(db.Integer, primary_key=True, nullable=False)

    context = Column(db.Integer, nullable=True)

    begin = Column(db.DateTime, nullable=False)

    end = Column(db.DateTime, nullable=False)

    visable = Column(db.Boolean, nullable=False)
