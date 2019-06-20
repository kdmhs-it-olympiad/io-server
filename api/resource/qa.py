from datetime import datetime
from pytz import timezone

from flask_restful import abort, fields, reqparse, Resource, marshal_with

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
    return dt.strftime('%Y년 %m월%d일 %H:%M')


qa_list_post_parser = reqparse.RequestParser()
qa_list_post_parser.add_argument('name', type=max_length(16), required=True, location='form')
qa_list_post_parser.add_argument('email', type=max_length(32), required=True, location='form')
qa_list_post_parser.add_argument('question', type=str, required=True, location='form')


qa_list_get_parser = reqparse.RequestParser()
qa_list_get_parser.add_argument('count', type=int, required=True)
qa_list_get_parser.add_argument('offset', type=int, required=True)

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
    def get(self):
        args = qa_list_get_parser.parse_args()

        qa_list = db.session \
            .query(QaModel) \
            .filter(QaModel.is_visable.is_(True)) \
            .limit(args.count) \
            .offset(args.offset) \
            .all()

        qa_list_str = []
        for i in qa_list:
            i.create_datetime = dt_to_str(i.create_datetime)
            qa_list_str.append(i)

        return {'qa': qa_list_str}


class QaResource(Resource):

    @marshal_with(qa_fields)
    def get(self, id):
        qa = db.session \
            .query(QaModel) \
            .filter(QaModel.id == id) \
            .first()

        if qa is None:
            abort(404, 'The article is not found.')

        qa.create_datetime = dt_to_str(qa.create_datetime)

        return qa

    def patch(self, id):
        args = qa_patch_parser.parse_args()

        qa = db.session \
            .query(QaModel) \
            .filter(QaModel.id == id) \
            .first()

        if qa is None:
            abort(404, 'The article is not found.')

        qa.answer = args.answer

        db.session.commit()

        return {'status': 'ok'}
