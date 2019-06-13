from api import server

from .calender import CalenderResource

api = server.flask_api

api.add_resource(CalenderResource, '/calender')
