import datetime
import uuid
from flask_restx import Namespace, Resource, fields, abort
from .security import sec_admin, sec_contractor
from apiv2 import db
from apiv2.models.User import User
from apiv2.models.Commit import Commit
from .datetimeparser import parse_datetime

apiCommitNs = Namespace('Commit', description="Commit resource endpoints.")

commit_schema = apiCommitNs.model(name='Commit', model={
    'creator_id': fields.String(required=True,
                                description='UUID of the creator User',
                                example=str(uuid.uuid4()),
                                attribute=lambda commit: commit.creator.uuid,
                                max_length=40),
    'date': fields.DateTime(required=False,
                            dt_format="iso8601",
                            default=datetime.datetime.utcnow,
                            description='Creation time in ISO8601 format, with UTC timestamp'),
    'lines_added': fields.Integer(required=True,
                                  description='Lines added in this commit'),
    'lines_removed': fields.Integer(required=True,
                                    description='Lines removed in this commit'),
    'description': fields.String(required=True,
                                 description='Short description of the commit'),
    'commit_id': fields.String(readonly=True, attribute='uuid',
                               descritpion="UUID of the Commit",
                               example=str(uuid.uuid4()),
                               max_length=40)
})


@apiCommitNs.response(409, "Conflict with data on the server. You most likely tried to use a value, that is already"
                           "taken, in a field with the 'unique' constraint.")
@apiCommitNs.response(403, "You do not have access to this resource. The authorization you provided is not sufficient.")
@apiCommitNs.response(401, "Authorization required. You did not provide any valid authentication.")
@apiCommitNs.response(404, "Commit not found")
@apiCommitNs.doc(security=['apikey'])
@apiCommitNs.param('commit_id', "ID of the desired commit", _in='path')
@apiCommitNs.route("/<string:commit_id>", endpoint='commit_find')
class ExistingCommitResource(Resource):
    @apiCommitNs.marshal_with(commit_schema, description="Requested commit")
    @apiCommitNs.doc(description="Get Commit by tis UUID")
    @sec_contractor
    def get(self, commit_id):
        return db.session.query(Commit).filter_by(uuid=commit_id).first_or_404()


@apiCommitNs.response(409, "Conflict with data on the server. You most likely tried to use a value, that is already"
                           "taken, in a field with the 'unique' constraint.")
@apiCommitNs.response(403, "You do not have access to this resource. The authorization you provided is not sufficient.")
@apiCommitNs.response(401, "Authorization required. You did not provide any valid authentication.")
@apiCommitNs.doc(security=['apikey'])
@apiCommitNs.route('/', endpoint='commit ')
class CommitResource(Resource):
    @apiCommitNs.marshal_with(commit_schema, description="List of all commits on the server", as_list=True)
    @apiCommitNs.doc(description="Get all Commits")
    @sec_contractor
    def get(self):
        return db.session.query(Commit).all()

    @apiCommitNs.marshal_with(commit_schema, description="Created commit", code=201)
    @apiCommitNs.doc(description="Create commit")
    @apiCommitNs.response(404, "User, who was supposed to be the creator of this commit, could not be found!")
    @apiCommitNs.expect(commit_schema, validate=True)
    @sec_admin
    def put(self):
        creator = db.session.query(User).filter_by(uuid=apiCommitNs.payload["creator_id"]).first_or_404()
        date = parse_datetime(apiCommitNs.payload.get('date'))
        new_commit = Commit(creator=creator,
                            description=apiCommitNs.payload["description"],
                            lines_added=apiCommitNs.payload['lines_added'],
                            lines_removed=apiCommitNs.payload['lines_removed'],
                            date=date)
        db.session.add(new_commit)
        db.session.commit()
        return new_commit, 201

