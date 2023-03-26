from flask import abort, jsonify


def abort_bad_json():
    abort(400, description="Missing fields in JSON data")


def add_error_handlers(endpoint):
    @endpoint.errorhandler(400)
    def bad_request(e):
        return jsonify(message=f"{e.description}"), 400

    @endpoint.errorhandler(404)
    def not_found(e):
        return jsonify(message=f"{e.description}"), 404

    @endpoint.errorhandler(403)
    def forbidden(e):
        return jsonify(message=f"{e.description}"), 403
