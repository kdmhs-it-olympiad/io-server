from datetime import datetime

from flask_restful import Resource, abort

from api import server
from api.model.calender import CalenderModel

db = server.db


class CalenderResource(Resource):
    def get(self):
        now_dt = datetime.now()
        now_calender = db.session \
            .query(CalenderModel) \
            .filter(now_dt >= CalenderModel.begin, now_dt <= CalenderModel.end, CalenderModel.visable.is_(True)) \
            .first()
        if now_calender is None:
            abort(404, message='There is no corresponding calender.')
        calender = {
            'id': now_calender.id,
            'begin': now_calender.begin.strftime("%Y-%m-%d %H:%M:%S"),
            'end': now_calender.end.strftime("%Y-%m-%d %H:%M:%S"),
            'context': now_calender.context
        }

        return calender
