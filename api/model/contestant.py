from sqlalchemy.dialects.mysql import ENUM

from api.model import db


class ContestantModel(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)

    name = db.Column(db.String(16), nullable=False)

    gender = db.Column(ENUM('male', 'female'), nullable=False)

    birth = db.Column(db.Date, nullable=False)

    agent_phone = db.Column(db.String(16), nullable=False)

    phone = db.Column(db.String(16), nullable=True)

    school = db.Column(db.String(64), nullable=True)

    grade = db.Column(db.Integer, nullable=True)

    klass = db.Column(db.Integer, nullable=True)

    zip_code = db.Column(db.String(8), nullable=False)

    address = db.Column(db.String(128), nullable=False)

    detail_address = db.Column(db.String(128), nullable=False)

    sector = db.Column(ENUM('programming', 'design', 'business'), nullable=False)

    photo = db.Column(db.String(64), nullable=True)

    password = db.Column(db.String(256), nullable=False)

    lunch_number = db.Column(db.Integer, nullable=False)