import os
import uuid
import werkzeug

from flask_restful import abort, reqparse, Resource

from api import server
from api.model.contestant import ContestantModel

from config import config


db = server.db
api = server.flask_api

ALLOWED_FILE_EXTENSOIN = ['image/jpeg', 'image/png', 'image/gif']
MAX_PHOTO_SIZE = 5242880


def max_length(max_length):
    def validate(s):
        if len(s) <= max_length:
            return s
        raise ValueError("String must be at least %i characters long" % max_length)
    return validate


contestant_parser = reqparse.RequestParser()
contestant_parser.add_argument('name', type=max_length(16), required=True, location='form')
contestant_parser.add_argument('gender', type=str, required=True, location='form')
contestant_parser.add_argument('birth', required=True)
contestant_parser.add_argument('agent_phone', type=max_length(16), required=True, location='form')
contestant_parser.add_argument('phone', type=max_length(16), required=True, location='form')
contestant_parser.add_argument('school', type=max_length(64), required=False, location='form')
contestant_parser.add_argument('grade', type=int, required=False, location='form')
contestant_parser.add_argument('klass', type=int, required=False, location='form')
contestant_parser.add_argument('zip_code', type=max_length(8), required=True, location='form')
contestant_parser.add_argument('address', type=max_length(128), required=True, location='form')
contestant_parser.add_argument('detail_address', type=max_length(128), required=True, location='form')
contestant_parser.add_argument('sector', type=str, required=True, location='form')
contestant_parser.add_argument('photo', type=werkzeug.datastructures.FileStorage, location='files', required=True)
contestant_parser.add_argument('password', type=str, required=True, location='form')
contestant_parser.add_argument('launch_number', type=int, required=True, location='form')


class ContestantResource(Resource):

    def post(self):
        args = contestant_parser.parse_args()

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
            password=args.password,
            launch_number=args.launch_number
        )

        db.session.add(contestant)
        db.session.commit()

        return {'status': 'ok'}