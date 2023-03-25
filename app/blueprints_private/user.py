from app import db
from flask import Blueprint, abort, jsonify, request, session
from sqlalchemy.exc import IntegrityError
from app.models.User import User

private_user_endpoint = Blueprint("private_user_endpoint", __name__)


def abort_bad_json():
    abort(400, description="Missing fields in JSON data")


@private_user_endpoint.errorhandler(400)
def bad_request(e):
    return jsonify(message=f"{e.description}"), 400


@private_user_endpoint.errorhandler(404)
def not_found(e):
    return jsonify(message=f"{e.description}"), 404


@private_user_endpoint.errorhandler(403)
def forbidden(e):
    return jsonify(message=f"{e.description}"), 403


@private_user_endpoint.route("/create", methods=["PUT"])
def add_user():
    """
    Adds user from JSON. ex.:
    {
        "name": "John",
        "surname": "Doe",
        "nick": "JD"
    }
    """
    data = request.get_json()
    try:
        new_user = User(data["nick"], data["name"], data["surname"])
        db.session.add(new_user)
        db.session.commit()
    except KeyError:
        abort_bad_json()
    except IntegrityError:
        return jsonify(message=f"Integrity error"), 409

    return jsonify(message="OK"), 200


@private_user_endpoint.route("/all", methods=["GET"])
def get_all_users():
    users = User.query.all()
    ret = []
    for user in users:
        ret.append({
            "nick": user.nick,
            "name": user.name,
            "surname": user.surname,
            "avatar_url": user.avatar_url,
            "uuid": user.uuid,
        })
    return jsonify(ret), 200
