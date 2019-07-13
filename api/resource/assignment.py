from datetime import datetime
from pytz import timezone
import hashlib
import os
import uuid
import werkzeug

from flask_restful import abort, fields, reqparse, Resource, marshal_with

from api import server
from api.model.calender import CalenderModel
from api.model.contestant import ContestantModel
from api.model.assignment import AssignmentModel

from config import config

db = server.db
api = server.flask_api

MAX_FILE_SIZE = 100000000
ALLOWED_FILE_EXTENSOIN = {
    'design': ['image/png', 'image/jpg', 'image/jpeg', 'application/zip'],
    'business': ['application/x-hwp', 'application/haansofthwp', 'application/vnd.hancom.hwp', 'application/pdf', 'application/octet-stream']
}

assignment_post_parser = reqparse.RequestParser()
assignment_post_parser.add_argument('assignment', type=werkzeug.datastructures.FileStorage, location='files', required=True)
assignment_post_parser.add_argument('agent_phone', type=str, required=True, location='form')
assignment_post_parser.add_argument('password', type=str, required=True, location='form')

assignment_get_parser = reqparse.RequestParser()
assignment_get_parser.add_argument('agent_phone', type=str, required=True, location='args')
assignment_get_parser.add_argument('password', type=str, required=True, location='args')


class AssignmentResource(Resource):
    def post(self):
        now_dt = datetime.now(timezone('Asia/Seoul'))

        calender_check = db.session \
            .query(CalenderModel) \
            .filter(
                now_dt >= CalenderModel.begin,
                now_dt <= CalenderModel.end,
                CalenderModel.status == 'submit_assignment'
            ) \
            .first()
        if calender_check is None:
            abort(406, message='It is not time to upload file.')

        args = assignment_post_parser.parse_args()

        print(args.assignment.content_type)
        contestant = db.session \
            .query(ContestantModel) \
            .filter(ContestantModel.agent_phone == args.agent_phone) \
            .first()

        if contestant is None:
            abort(404, message='Not Founded agent_phone number.')

        password_hash = hashlib.sha256()
        password_hash.update(args.password.encode())
        password_hash = password_hash.hexdigest()

        if contestant.password != password_hash:
            abort(401, message='Wrong password.')

        if contestant.sector == 'programming':
            abort(406, message='Programming sector can not submit assignments.')

        if args.assignment.content_type not in ALLOWED_FILE_EXTENSOIN[contestant.sector]:
            abort(400, message='Only {} photos can be uploaded.'.format(ALLOWED_FILE_EXTENSOIN[contestant.sector]))

        args.assignment.seek(0, os.SEEK_END)
        if args.assignment.tell() > MAX_FILE_SIZE:
            abort(413, message='The file is too large.')

        args.assignment.seek(0)
        args.assignment.filename = '{}.{}'.format(str(uuid.uuid4()), args.assignment.content_type.split('/')[-1])
        args.assignment.save('{}/{}/{}'.format(config.STATIC_FILE_PATH, 'assignment', args.assignment.filename))

        assignment = AssignmentModel(
            contestant_id=contestant.id,
            file=args.assignment.filename
        )

        db.session.add(assignment)
        db.session.commit()

        return {'status': 'ok'}

    def get(self):
        args = assignment_get_parser.parse_args()

        contestant = db.session \
            .query(ContestantModel) \
            .filter(ContestantModel.agent_phone == args.agent_phone) \
            .first()

        if contestant is None:
            abort(404, message='Not Founded agent_phone number.')

        password_hash = hashlib.sha256()
        password_hash.update(args.password.encode())
        password_hash = password_hash.hexdigest()

        if contestant.password != password_hash:
            abort(401, message='Wrong password.')

        if contestant.sector == 'programming':
            abort(406, message='Programming sector can not submit assignments.')

        if contestant.assignment == []:
            return {'assignment': None}

        return {'assignment': contestant.assignment[0].file}

    def patch(self):
        now_dt = datetime.now(timezone('Asia/Seoul'))

        calender_check = db.session \
            .query(CalenderModel) \
            .filter(
            now_dt >= CalenderModel.begin,
            now_dt <= CalenderModel.end,
            CalenderModel.status == 'submit_assignment'
        ) \
            .first()
        if calender_check is None:
            abort(406, message='It is not time to upload file.')

        args = assignment_post_parser.parse_args()

        contestant = db.session \
            .query(ContestantModel) \
            .filter(ContestantModel.agent_phone == args.agent_phone) \
            .first()

        if contestant is None:
            abort(404, message='Not Founded agent_phone number.')

        password_hash = hashlib.sha256()
        password_hash.update(args.password.encode())
        password_hash = password_hash.hexdigest()

        if contestant.password != password_hash:
            abort(401, message='Wrong password.')

        if contestant.sector == 'programming':
            abort(406, message='Programming sector can not submit assignments.')

        if contestant.assignment == []:
            abort(404, message='Not Founded assignments.')

        if args.assignment.content_type not in ALLOWED_FILE_EXTENSOIN[contestant.sector]:
            abort(400, message='Only {} photos can be uploaded.'.format(ALLOWED_FILE_EXTENSOIN[contestant.sector]))

        args.assignment.seek(0, os.SEEK_END)
        if args.assignment.tell() > MAX_FILE_SIZE:
            abort(413, message='The file is too large.')

        args.assignment.seek(0)
        args.assignment.filename = '{}.{}'.format(str(uuid.uuid4()), args.assignment.content_type.split('/')[-1])
        args.assignment.save('{}/{}/{}'.format(config.STATIC_FILE_PATH, 'assignment', args.assignment.filename))

        contestant.assignment[0].file = args.assignment.filename

        db.session.commit()

        return {'assignment': contestant.assignment[0].file}
