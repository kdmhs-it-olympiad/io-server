from api.model import db


class AdminAccountModel(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)

    username = db.Column(db.String(32), nullable=False)

    password = db.Column(db.String(256), nullable=False)
