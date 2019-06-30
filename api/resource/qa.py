from datetime import datetime
from pytz import timezone

from flask_restful import abort, fields, reqparse, Resource, marshal_with
from flask_jwt_extended import jwt_optional, get_jwt_identity, jwt_required

from api import server
from api.model.qa import QaModel


db = server.db
api = server.flask_api


def max_length(max_length):
    def validate(s):
        if len(s) <= max_length:
            return s
        raise ValueError("String must be at least %i characters long" % max_length)
    return validate


def dt_to_str(dt):
    return dt.strftime('%Y-%m-%d %H:%M')


qa_list_post_parser = reqparse.RequestParser()
qa_list_post_parser.add_argument('name', type=max_length(16), required=True, location='form')
qa_list_post_parser.add_argument('email', type=max_length(32), required=True, location='form')
qa_list_post_parser.add_argument('question', type=str, required=True, location='form')


qa_list_get_parser = reqparse.RequestParser()
qa_list_get_parser.add_argument('count', type=int, required=False)
qa_list_get_parser.add_argument('offset', type=int, required=False)

qa_patch_parser = reqparse.RequestParser()
qa_patch_parser.add_argument('answer', type=str, required=True, location='form')

qa_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String,
    'question': fields.String,
    'answer': fields.String,
    'create_datetime': fields.String
}

qa_list_fields = {'qa': fields.Nested(qa_fields)}


class QaListResource(Resource):

    def post(self):
        args = qa_list_post_parser.parse_args()

        qa = QaModel(
            name=args.name,
            email=args.email,
            question=args.question,
            create_datetime=datetime.now(timezone('Asia/Seoul'))
        )

        db.session.add(qa)
        db.session.commit()

        return {'status': 'ok'}

    @marshal_with(qa_list_fields)
    @jwt_optional
    def get(self):
        admin = get_jwt_identity()
        args = qa_list_get_parser.parse_args()

        if args.count is None:
            args.count = 10
        if args.offset is None:
            args.offset = 0

        qa_list = db.session \
            .query(QaModel) \
            .filter(QaModel.is_visable.is_(True)) \

        if not admin:
            qa_list = qa_list.filter(QaModel.answer.isnot(None)) \
                             .limit(args.count) \
                             .offset(args.offset)

        qa_list = qa_list.all()

        qa_list_str = []
        for i in qa_list:
            i.create_datetime = dt_to_str(i.create_datetime)
            qa_list_str.append(i)

        return {'qa': qa_list_str}


class QaResource(Resource):

    @marshal_with(qa_fields)
    @jwt_required
    def get(self, id):
        qa = db.session \
            .query(QaModel) \
            .filter(QaModel.id == id) \
            .first()

        if qa is None:
            abort(404, message='The article is not found.')

        qa.create_datetime = dt_to_str(qa.create_datetime)

        return qa

    @jwt_required
    def patch(self, id):
        args = qa_patch_parser.parse_args()

        qa = db.session \
            .query(QaModel) \
            .filter(QaModel.id == id) \
            .first()

        if qa is None:
            abort(404, message='The article is not found.')

        qa.answer = args.answer

        db.session.commit()

        return {'status': 'ok'}
