import hashlib

from flask_restful import abort, fields, reqparse, marshal_with, Resource
from flask_jwt_extended import create_access_token

from api import server
from api.model.admin_account import AdminAccountModel


db = server.db
api = server.flask_api


def max_length(max_length):
    def validate(s):
        if len(s) <= max_length:
            return s
        raise ValueError("String must be at least %i characters long" % max_length)
    return validate


auth_post_parser = reqparse.RequestParser()
auth_post_parser.add_argument('username', type=max_length(32), required=True, location='form')
auth_post_parser.add_argument('password', type=str, required=True, location='form')

auth_fileds = {
    'access_token': fields.String
}


class AuthResource(Resource):

    @marshal_with(auth_fileds)
    def post(self):
        args = auth_post_parser.parse_args()

        admin_account = db.session \
            .query(AdminAccountModel) \
            .filter(AdminAccountModel.username == args.username) \
            .first()

        if admin_account is None:
            abort(404, message='Account does not exist')

        password_hash = hashlib.sha256()
        password_hash.update(args.password.encode())
        password_hash = password_hash.hexdigest()

        if password_hash != admin_account.password:
            abort(401, message='Wrong password')

        access_token = create_access_token(identity=args.username)

        return {'access_token': access_token}
