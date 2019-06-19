from datetime import datetime
from pytz import timezone
import hashlib
import os
import uuid
import werkzeug

from flask_restful import abort, fields, reqparse, Resource, marshal_with

from api import server
from api.model.contestant import ContestantModel
from api.model.calender import CalenderModel

from config import config


db = server.db
api = server.flask_api

ALLOWED_FILE_EXTENSOIN = ['image/jpeg', 'image/png', 'image/gif']
MAX_PHOTO_SIZE = 5242880

PHOTO_FILE_PATH = '/photo/'


def max_length(max_length):
    def validate(s):
        if len(s) <= max_length:
            return s
        raise ValueError("String must be at least %i characters long" % max_length)
    return validate


contestant_post_parser = reqparse.RequestParser()
contestant_post_parser.add_argument('name', type=max_length(16), required=True, location='form')
contestant_post_parser.add_argument('gender', type=str, required=True, location='form')
contestant_post_parser.add_argument('birth', required=True)
contestant_post_parser.add_argument('agent_phone', type=max_length(16), required=True, location='form')
contestant_post_parser.add_argument('phone', type=max_length(16), required=False, location='form')
contestant_post_parser.add_argument('school', type=max_length(64), required=False, location='form')
contestant_post_parser.add_argument('grade', type=int, required=False, location='form')
contestant_post_parser.add_argument('klass', type=int, required=False, location='form')
contestant_post_parser.add_argument('zip_code', type=max_length(8), required=True, location='form')
contestant_post_parser.add_argument('address', type=max_length(128), required=True, location='form')
contestant_post_parser.add_argument('detail_address', type=max_length(128), required=True, location='form')
contestant_post_parser.add_argument('sector', type=str, required=True, location='form')
contestant_post_parser.add_argument('photo', type=werkzeug.datastructures.FileStorage, location='files', required=True)
contestant_post_parser.add_argument('password', type=str, required=True, location='form')
contestant_post_parser.add_argument('launch_number', type=int, required=True, location='form')

contestant_get_parser = reqparse.RequestParser()
contestant_get_parser.add_argument('agent_phone', type=str, required=True, location='args')
contestant_get_parser.add_argument('password', type=str, required=True, location='args')

contestant_patch_parser = reqparse.RequestParser()
contestant_patch_parser.add_argument('photo', type=werkzeug.datastructures.FileStorage, location='files', required=True)
contestant_patch_parser.add_argument('agent_phone', type=str, required=True, location='form')
contestant_patch_parser.add_argument('password', type=str, required=True, location='form')

contestant_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'gender': fields.String,
    'agent_phone': fields.String,
    'phone': fields.String,
    'school': fields.String,
    'grade': fields.Integer,
    'klass': fields.Integer,
    'sector': fields.String,
    'photo': fields.String
}


class ContestantResource(Resource):

    def post(self):
        now_dt = datetime.now(timezone('Asia/Seoul'))

        calender_check = db.session \
            .query(CalenderModel) \
            .filter(now_dt >= CalenderModel.begin, now_dt <= CalenderModel.end, CalenderModel.status == 'applying') \
            .first()
        if calender_check is None:
            abort(406, message='It is not time to apply.')

        args = contestant_post_parser.parse_args()

        contestant_check = db.session \
            .query(ContestantModel) \
            .filter(ContestantModel.agent_phone == args.agent_phone) \
            .first()

        if contestant_check is not None:
            abort(409, message='The agent_phone number already exists.')

        if args.photo.content_type not in ALLOWED_FILE_EXTENSOIN:
            abort(400, message='Only png and jpg photos can be uploaded.')

        args.photo.seek(0, os.SEEK_END)
        if args.photo.tell() > MAX_PHOTO_SIZE:
            abort(413, message='The photo is too large.')

        args.photo.seek(0)
        args.photo.filename = '{}.{}'.format(str(uuid.uuid4()), args.photo.content_type.split('/')[-1])
        args.photo.save('{}/{}'.format(config.STATIC_FILE_PATH, args.photo.filename))

        password_hash = hashlib.sha256()
        password_hash.update(args.password.encode())
        password_hash = password_hash.hexdigest()

        contestant = ContestantModel(
            name=args.name,
            gender=args.gender,
            birth=args.birth,
            agent_phone=args.agent_phone,
            phone=args.phone,
            school=args.school,
            grade=args.grade,
            klass=args.klass,
            zip_code=args.zip_code,
            address=args.address,
            detail_address=args.detail_address,
            sector=args.sector,
            photo=args.photo.filename,
            password=password_hash,
            launch_number=args.launch_number
        )

        db.session.add(contestant)
        db.session.commit()

        return {'status': 'ok'}

    @marshal_with(contestant_fields)
    def get(self):
        args = contestant_get_parser.parse_args()

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

        if contestant.photo is not None:
            contestant.photo = '{}{}'.format(PHOTO_FILE_PATH, contestant.photo)

        return contestant

    def patch(self):
        now_dt = datetime.now(timezone('Asia/Seoul'))

        calender_check = db.session \
            .query(CalenderModel) \
            .filter(now_dt >= CalenderModel.begin, now_dt <= CalenderModel.end, CalenderModel.status == 'applying') \
            .first()
        if calender_check is None:
            abort(406, message='It is not time to apply.')

        args = contestant_patch_parser.parse_args()

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

        if args.photo.content_type not in ALLOWED_FILE_EXTENSOIN:
            abort(400, message='Only png and jpg photos can be uploaded.')

        args.photo.seek(0, os.SEEK_END)
        if args.photo.tell() > MAX_PHOTO_SIZE:
            abort(413, message='The photo is too large.')

        args.photo.seek(0)
        args.photo.filename = '{}.{}'.format(str(uuid.uuid4()), args.photo.content_type.split('/')[-1])
        args.photo.save('{}/{}'.format(config.STATIC_FILE_PATH, args.photo.filename))

        db.session \
            .query(ContestantModel) \
            .filter(ContestantModel.agent_phone == args.agent_phone) \
            .update({'photo': args.photo.filename}, synchronize_session=False)

        db.session.commit()

        return {'photo': '{}{}'.format(PHOTO_FILE_PATH, args.photo.filename)}
