from app import db
from flask import Blueprint, abort, jsonify, request, session
from sqlalchemy.exc import IntegrityError
from app.models.User import User
from app.models.Commit import Commit
from datetime import datetime
from dateutil import parser as dateparser
from app.blueprints.errorhandling import abort_bad_json
import app.blueprints.errorhandling as json_error_handler

private_commit_endpoint = Blueprint("private_commit_endpoint", __name__)
json_error_handler.add_error_handlers(private_commit_endpoint)


@private_commit_endpoint.route("/create", methods=["PUT"])
def create_commit():
    """
    Create commit from JSON. ex.:
    {
        "creator_uuid": "uuid",
        "description": "description",
        "datetime": "datetime"
    }
    """
    data: dict = request.get_json()
    try:
        date = dateparser.isoparse(data["datetime"]) if "datetime" in data else None
        creator = User.query.filter_by(uuid=data["creator_uuid"]).first_or_404(description="Creator user not found")
        new_commit = Commit(creator,
                            description=data["description"],
                            date=date)
        db.session.add(new_commit)
        db.session.commit()
    except KeyError:
        abort_bad_json()
    except dateparser.ParserError:
        abort(400, description=f"{data['datetime']} could not be parsed into a datetime object. Please use RFC 3339 or "
                               f"ISO 8601 date format!")

    return jsonify(message="OK"), 200


