from functools import wraps
from flask import request, abort

def need_contractor_id(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        contractor_id = request.headers.get("x-contractor-id")
        if contractor_id is None:
            pass
            # TODO FINISH THIS AUTH SHITHOLE YOU GOT YOURSELF INTO!
