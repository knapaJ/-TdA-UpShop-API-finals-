from app import db
from flask import Blueprint, abort, jsonify, request, session
from sqlalchemy.exc import IntegrityError
from app.models.User import User
from app.blueprints.errorhandling import abort_bad_json
import app.blueprints.errorhandling as json_error_handler


user_endpoint = Blueprint("user_endpoint", __name__)
json_error_handler.add_error_handlers(user_endpoint)


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
