from sqlalchemy.schema import Column

from api.model import db


class AdminAccountModel(db.Model):
    id = Column(db.Integer, primary_key=True, nullable=False)

    username = Column(db.String(32), nullable=False)

    password = Column(db.String(256), nullable=False)
