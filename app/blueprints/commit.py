from app import db
from flask import Blueprint, abort, jsonify, request, current_app
from sqlalchemy.exc import IntegrityError
from app.models.User import User
from app.models.Commit import Commit
from datetime import datetime
from dateutil import parser as dateparser

TOO_MUCH = 40

commit_endpoint = Blueprint("commit_endpoint", __name__)


def abort_bad_json():
    abort(400, description="Missing fields in JSON data")


@commit_endpoint.errorhandler(400)
def bad_request(e):
    return jsonify(message=f"{e.description}"), 400


@commit_endpoint.errorhandler(404)
def not_found(e):
    return jsonify(message=f"{e.description}"), 404


@commit_endpoint.errorhandler(403)
def forbidden(e):
    return jsonify(message=f"{e.description}"), 403


@commit_endpoint.route("", methods=["GET"])
def get_commits():
    ret = []
    commits = Commit.query.order_by("date").all()
    for commit in commits:
        ret.append({
            "creator_uuid": commit.creator.uuid,
            "description": commit.description,
            "datetime": commit.date.isoformat()
        })
    current_app.logger.warn(f"{request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)} "
                            f"made a wide request for ALL COMMITS! "
                            f"This may put unnecessary strain on our backend!")
    return jsonify(ret), 200


@commit_endpoint.route("/byuser/<user_uuid>", methods=["GET"])
def get_commits_by_user(user_uuid):
    user = User.query.filter_by(uuid=user_uuid).first_or_404(description="User not found")
    ret = []
    for commit in user.commits:
        ret.append({
            "creator_uuid": commit.creator.uuid,
            "description": commit.description,
            "uuid": commit.uuid,
            "datetime": commit.date.isoformat(),
        })
    if len(ret) > TOO_MUCH:
        current_app.logger.warn(f"{request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)} "
                                f"made a wide request for more than {TOO_MUCH} commits at once!"
                                f" If this is a repeated occurrence, our servers might not withstand it!")
    return jsonify(ret), 200


@commit_endpoint.route("/<start>", methods=["GET"], defaults={"end": None})
@commit_endpoint.route("/<start>/<end>", methods=["GET"])
def get_commits_by_time(start, end):
    try:
        start_date = dateparser.isoparse(start)
        end_date = dateparser.isoparse(end) if end is not None else None
        if end_date is not None and end_date < start_date:
            abort(400, description="Start date can not be before end date!")
        commits = []
        if end_date is not None:
            commits = db.session.query(Commit).filter(Commit.date >= start_date, Commit.date <= end_date)\
                      .order_by("date").all()
        else:
            commits = db.session.query(Commit).filter(Commit.date >= start_date).order_by("date").all()
        ret = []
        for commit in commits:
            ret.append({
                "creator_uuid": commit.creator.uuid,
                "description": commit.description,
                "uuid": commit.uuid,
                "datetime": commit.date.isoformat(),
            })
        if len(ret) > TOO_MUCH:
            current_app.logger.warn(f"{request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)} "
                                    f"made a wide request for more than {TOO_MUCH} commits at once!"
                                    f" If this is a repeated occurrence, our servers might not withstand it!")
        return jsonify(ret), 200
    except dateparser.ParserError:
        abort(400, description="Date parts of the url can not be parsed!")

