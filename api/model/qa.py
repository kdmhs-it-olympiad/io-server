from api.model import db


class QaModel(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)

    name = db.Column(db.String(16), nullable=False)

    email = db.Column(db.String(32), nullable=False)

    question = db.Column(db.Text, nullable=False)

    answer = db.Column(db.Text, nullable=True)

    create_datetime = db.Column(db.DateTime, nullable=False)

    is_visable = db.Column(db.Boolean, nullable=False, default=True)
