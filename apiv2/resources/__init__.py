from flask_restx import Api
from .User import apiUserNs

auth = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'x-contractor-id',
    },
}

api = Api(
    title="VCS commit monitoring API.",
    version="v2",
    description="API for monitoring and reporting stats about the internal VCS system. Any piece of information"
                "obtained from this system is strictly confidential and as such should not be shared with any "
                "unauthorised personnel!",
    authorizations=auth,
)

api.add_namespace(apiUserNs, path="/user")
