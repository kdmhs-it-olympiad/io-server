from datetime import datetime
from pytz import timezone

from flask_restful import Resource, abort, fields, marshal_with

from api import server
from api.model.calender import CalenderModel

db = server.db

calender_fileds = {
    'id': fields.Integer,
    'begin': fields.DateTime,
    'end': fields.DateTime,
    'status': fields.String,
    'context': fields.String
}


class CalenderResource(Resource):

    @marshal_with(calender_fileds)
    def get(self):
        now_dt = datetime.now(timezone('Asia/Seoul'))
        now_calender = db.session \
            .query(CalenderModel) \
            .filter(now_dt >= CalenderModel.begin, now_dt <= CalenderModel.end, CalenderModel.visable.is_(True)) \
            .first()
        if now_calender is None:
            abort(404, message='There is no corresponding calender.')

        return now_calender