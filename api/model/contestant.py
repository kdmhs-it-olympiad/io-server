from sqlalchemy.schema import Column
from sqlalchemy.dialects.mysql import ENUM

from api.model import db


class ContestantModel(db.Model):
    id = Column(db.Integer, primary_key=True, nullable=False)

    name = Column(db.String(16), nullable=False)

    gender = Column(ENUM('male', 'female'), nullable=False)

    birth = Column(db.DateTime, nullable=False)

    agent_phone = Column(db.String(16), nullable=False)

    phone = Column(db.String(16), nullable=False)

    school = Column(db.String(64), nullable=True)

    grade = Column(db.Integer, nullable=True)

    klass = Column(db.Integer, nullable=True)

    zip_code = Column(db.String(8), nullable=False)

    address = Column(db.String(128), nullable=False)

    detail_address = Column(db.String(128), nullable=False)

    sector = Column(ENUM('programming', 'design', 'business'), nullable=False)

    photo = Column(db.String(64), nullable=False)

    password = Column(db.String(256), nullable=False)

    launch_number = Column(db.Integer, nullable=False)
