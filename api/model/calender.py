from sqlalchemy.schema import Column
from sqlalchemy.dialects.mysql import ENUM

from api.model import db


class CalenderModel(db.Model):
    id = Column(db.Integer, primary_key=True, nullable=False)

    context = Column(db.String(32), nullable=True)

    begin = Column(db.DateTime, nullable=False)

    end = Column(db.DateTime, nullable=False)

    status = Column(ENUM('applying', 'design_1st_submitting', 'design_1st_announcing', 'waiting_for_contest',
                         'contesting', 'final_submitting', 'end'))

    visable = Column(db.Boolean, nullable=False)
