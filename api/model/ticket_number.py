from api.model import db


class TicketNumberModel(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)

    contestant_id = db.Column(db.Integer, db.ForeignKey('contestant_model.id'), nullable=False)

    ticket_number = db.Column(db.Integer, nullable=False)

    contestant = db.relationship('ContestantModel', backref=db.backref('ticket', lazy=True))
