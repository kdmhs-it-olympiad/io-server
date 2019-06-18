from sqlalchemy.schema import Column

from api.model import db


class QaModel(db.Model):
    id = Column(db.Integer, primary_key=True, nullable=False)

    name = Column(db.String(16), nullable=False)

    email = Column(db.String(32), nullable=False)

    title = Column(db.String(256), nullable=False)

    context = Column(db.Text, nullable=False)

    create_datetime = Column(db.DateTime, nullable=False)

    is_visable = Column(db.Boolean, nullable=False, default=True)
