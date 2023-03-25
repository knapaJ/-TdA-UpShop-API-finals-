from app import db
from flask import Blueprint, abort, jsonify, request, session
from sqlalchemy.exc import IntegrityError
from app.models.User import User


user_endpoint = Blueprint("user_endpoint", __name__)


def abort_bad_json():
    abort(400, description="Missing fields in JSON data")


@user_endpoint.errorhandler(400)
def bad_request(e):
    return jsonify(message=f"{e.description}"), 400


@user_endpoint.errorhandler(404)
def not_found(e):
    return jsonify(message=f"{e.description}"), 404


@user_endpoint.errorhandler(403)
def forbidden(e):
    return jsonify(message=f"{e.description}"), 403


@user_endpoint.route("/<string:uuid>", methods=["GET"])
def get_user(uuid: str):
    user = User.query.filter_by(uuid=uuid).first_or_404(description="User not found")
    return jsonify({
        "name": user.name,
        "surname": user.surname,
        "uuid": user.uuid,
        "nick": user.nick,
        "avatar_url": user.avatar_url
    }), 200
