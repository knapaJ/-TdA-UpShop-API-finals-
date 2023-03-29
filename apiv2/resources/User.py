import uuid
from flask_restx import Namespace, Resource, fields
from .security import sec_admin, sec_contractor
from apiv2 import db
from apiv2.models.User import User

apiUserNs = Namespace('User', description="User reading and editing.")

user_schema = apiUserNs.model(name='User', model={
    'name': fields.String(required=True,
                          description='User\'s first name.',
                          example='John',
                          max_length=50),
    'surname': fields.String(required=True,
                             description='User\'s last name.',
                             example='Doe',
                             max_length=50),
    'nick': fields.String(required=True, min_length=3,
                          description="Unique nick of the user.",
                          example="JayDee",
                          max_length=30),
    'avatar_url': fields.String(required=False,
                                description='URL of the user\'s avatar, located on our CDN.',
                                example='https://picsum.photos/seed/paisdpaishdpai/200'),
    'userID': fields.String(readonly=True, attribute='uuid',
                            description='User\'s UUID.',
                            example=str(uuid.uuid4()),
                            max_length=40)
})


@apiUserNs.response(403, "You do not have access to this resource. The authorization you provided is not sufficient.")
@apiUserNs.response(401, "Authorization required. You did not provide any valid authentication.")
@apiUserNs.param("user_id", "ID of the desired user", _in="path")
@apiUserNs.doc(security=['apikey'])
@apiUserNs.route("/<string:user_id>", endpoint='user_find')
class ExistingUserResource(Resource):
    @apiUserNs.doc(description="Get user by his userID")
    @apiUserNs.response(404, "User not found")
    # @apiUserNs.response(401, "Authorization required.")
    # @apiUserNs.response(403, "You do not have access to this resource")
    @sec_contractor
    @apiUserNs.marshal_with(user_schema, description="User with the according UUID.")
    def get(self, user_id):
        return db.session.query(User).filter_by(uuid=user_id).first_or_404(description="User not found")

    @apiUserNs.doc(description="Edit user")
    @apiUserNs.expect(user_schema, validate=True)
    # @apiUserNs.response(401, "Authorization required.")
    # @apiUserNs.response(403, "You do not have access to this resource")
    @apiUserNs.response(404, "User not found")
    @apiUserNs.response(409, "Database conflict")
    @sec_admin
    @apiUserNs.marshal_with(user_schema, description="Edited user", code=201)
    def post(self, user_id):
        user = db.session.query(User).filter_by(uuid=user_id).first_or_404(description="User not found")
        user.nick = apiUserNs.payload["nick"]
        user.name = apiUserNs.payload["name"]
        user.surname = apiUserNs.payload["surname"]
        db.session.add(user)
        db.session.commit()
        return user, 201


@apiUserNs.response(403, "You do not have access to this resource. The authorization you provided is not sufficient.")
@apiUserNs.response(401, "Authorization required. You did not provide any valid authentication.")
@apiUserNs.doc(security=['apikey'])
@apiUserNs.route("/", endpoint='user')
class UserResource(Resource):
    @apiUserNs.doc(description="Add new user")
    @apiUserNs.expect(user_schema, validate=True)
    @apiUserNs.marshal_with(user_schema, description="Created user", code=201)
    @sec_admin
    def put(self):
        new_user = User(nick=apiUserNs.payload["nick"],
                        name=apiUserNs.payload["name"],
                        surname=apiUserNs.payload["surname"])
        db.session.add(new_user)
        db.session.commit()
        return new_user, 201

    @apiUserNs.doc(description="List all users")
    @apiUserNs.marshal_with(user_schema, as_list=True, description="List of all users in database")
    @sec_contractor
    def get(self):
        users = db.session.query(User).all()
        return users, 200

