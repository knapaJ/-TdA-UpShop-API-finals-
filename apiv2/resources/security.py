from functools import wraps
from flask import request, abort, current_app
from enum import IntEnum


class AccessLevel(IntEnum):
    CONTRACTOR = 1
    ADMIN = 2


def need_auth(level: AccessLevel):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            auth_header = request.headers.get("x-access-token")
            if not auth_header:
                abort(401)

            req_level = get_level_from_token(auth_header)
            if not req_level >= level:
                abort(403)
            return f(*args, **kwargs)
        return wrapped
    return decorator


def get_level_from_token(token: str) -> AccessLevel:
    master_token = current_app.config.get("K_MASTER_TOKEN")
    if not master_token:
        master_token = "dev"
    if token == master_token:
        return AccessLevel.ADMIN

    contractor_tokens: list = current_app.config.get("K_CONTRACTOR_TOKEN_LIST")
    if not contractor_tokens:
        contractor_tokens = {"dev-user": "DEVELOPMENT-USER"}
    if token in contractor_tokens:
        return AccessLevel.CONTRACTOR
    abort(403)


sec_admin = need_auth(AccessLevel.ADMIN)
sec_contractor = need_auth(AccessLevel.CONTRACTOR)
