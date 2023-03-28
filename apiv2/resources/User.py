import uuid
from flask_restx import Namespace, Resource, fields, reqparse, inputs
from flask import request
from apiv2 import db
from apiv2.models.User import User

apiUserNs = Namespace('User', description="User reading and editing.")

user_schema = apiUserNs.model(name='User', model={
    'name': fields.String(required=True,
                          description='User\'s first name.',
                          example='John'),
    'surname': fields.String(required=True,
                             description='User\'s last name.',
                             example='Doe'),
    'nick': fields.String(required=True, min_length=3,
                          description="Unique nick of the user.",
                          example="JayDee"),
    'avatar_url': fields.String(required=False,
                                description='URL of the user\'s avatar, located on our CDN.',
                                example='https://picsum.photos/seed/paisdpaishdpai/200'),
    'userID': fields.String(readonly=True, attribute='uuid',
                            description='User\'s UUID.',
                            example=str(uuid.uuid4()))
})


@apiUserNs.route("/<string:user_id>", endpoint='user_find')
@apiUserNs.param("user_id", "ID of the desired user", _in="path")
@apiUserNs.doc(security=['apikey'])
class UserResource(Resource):
    @apiUserNs.doc(tags=['External'])
    @apiUserNs.doc(description="Get user by his userID")
    @apiUserNs.response(404, "User not found")
    @apiUserNs.marshal_with(user_schema, description="User with the according UUID.")
    def get(self, user_id):
        return db.session.query(User).filter_by(uuid=user_id).first_or_404(description="User not found")

    @apiUserNs.doc(description="Edit user")
    @apiUserNs.expect(user_schema, validate=True)
    @apiUserNs.marshal_with(user_schema, description="Edited user", code=201)
    def post(self, user_id):
        user = db.session.query(User).filter_by(uuid=user_id).first_or_404(description="User not found")
        user.nick = apiUserNs.payload["nick"]
        user.name = apiUserNs.payload["name"]
        user.surname = apiUserNs.payload["surname"]
        db.session.add(user)
        db.session.commit()
        return user, 201
