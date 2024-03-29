from api import server

from .calender import CalenderResource
from .contestant import ContestantResource, ContestantListResource
from .qa import QaResource, QaListResource
from .auth import AuthResource
from .assignment import AssignmentResource

api = server.flask_api

api.add_resource(CalenderResource, '/calender')
api.add_resource(ContestantResource, '/contestant')
api.add_resource(ContestantListResource, '/contestant/list')
api.add_resource(QaListResource, '/qa')
api.add_resource(QaResource, '/qa/<int:id>')
api.add_resource(AuthResource, '/auth')
api.add_resource(AssignmentResource, '/assignment')