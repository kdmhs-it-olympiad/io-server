from api import server

from .calender import CalenderResource
from .contestant import ContestantResource

api = server.flask_api

api.add_resource(CalenderResource, '/calender')
api.add_resource(ContestantResource, '/contestant')