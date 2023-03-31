import requests
import seeder.utils as utils
import json


def HTTPE2dict(e: requests.HTTPError):
    return json.loads(e.response.text)


def handle_400(e: requests.HTTPError):
    print(f'400 Bad Request: {HTTPE2dict(e)["message"]}')
    print(HTTPE2dict(e)["message"])
    exit(1)


def handle_403(e: requests.HTTPError):
    print(f'404 Not Found: {HTTPE2dict(e)["message"]}')
    exit(1)


def handle_404(e: requests.HTTPError):
    print(f'404 Not Found: {HTTPE2dict(e)["message"]}')
    utils.user_list = utils.sync_users()


def handle_500(e: requests.HTTPError):
    print(f'500 Internal Server Error: {HTTPE2dict(e)["message"]}')
    exit(1)
