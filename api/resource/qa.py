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


qa_list_post_parser = reqparse.RequestParser()
qa_list_post_parser.add_argument('name', type=max_length(16), required=True, location='form')
qa_list_post_parser.add_argument('email', type=max_length(32), required=True, location='form')
qa_list_post_parser.add_argument('title', type=max_length(256), required=True, location='form')
qa_list_post_parser.add_argument('context', type=str, required=True, location='form')


qa_list_get_parser = reqparse.RequestParser()
qa_list_get_parser.add_argument('count', type=int, required=True)
qa_list_get_parser.add_argument('offset', type=int, required=True)

qa_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String,
    'title': fields.String,
    'context': fields.String,
    'create_datetime': fields.DateTime
}

qa_list_fields = {'qa': fields.Nested(qa_fields)}


class QaListResource(Resource):

    def post(self):
        args = qa_list_post_parser.parse_args()

        qa = QaModel(
            name=args.name,
            email=args.email,
            title=args.title,
            context=args.context,
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

        return {'qa': qa_list}


class QaResource(Resource):

    @marshal_with(qa_fields)
    def get(self, id):
        qa = db.session \
            .query(QaModel) \
            .filter(QaModel.id == id) \
            .first()

        if qa is None:
            abort(404, 'The article is not found.')

        return qa
