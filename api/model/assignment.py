from api.model import db


class AssignmentModel(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)

    contestant_id = db.Column(db.Integer, db.ForeignKey('contestant_model.id'), nullable=False)

    file = db.Column(db.String(256), nullable=True)

    category = db.relationship('ContestantModel', backref=db.backref('assignment', lazy=True))
