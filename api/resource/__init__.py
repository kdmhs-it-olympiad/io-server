from api import server

from .calender import CalenderResource
from .contestant import ContestantResource
from .qa import QaResource, QaListResource

api = server.flask_api

api.add_resource(CalenderResource, '/calender')
api.add_resource(ContestantResource, '/contestant')
api.add_resource(QaListResource, '/qa')
api.add_resource(QaResource, '/qa/<int:id>')