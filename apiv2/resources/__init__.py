from flask_restx import Api
from .User import apiUserNs
from .Commit import apiCommitNs
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

auth = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'x-access-token',
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


@api.errorhandler(IntegrityError)
def conflict(error):
    return {"message": "Edited or created resource is in direct conflict with current server state."}, 409


@api.errorhandler(SQLAlchemyError)
def db_error(error):
    return {'message': f'An error occurred in the database: {error}'}, 500


api.add_namespace(apiUserNs, path="/user")
api.add_namespace(apiCommitNs, path='/commit')
