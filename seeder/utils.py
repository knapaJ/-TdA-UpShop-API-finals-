from seeder.models import User, Commit
from seeder.config import *
import requests
import random

user_list = []


def sync_users():
    response: requests.Response = requests.get(USER_URL, headers=HEADER)
    response.raise_for_status()
    # extract the userIDs from the response
    return [user['userID'] for user in response.json()]


def r_user_factory() -> requests.Response:
    ret = requests.put(USER_URL, json=User.fake().dump(), headers=HEADER)
    if ret.ok:
        user_list.append(ret.json()['userID'])
    return ret


def r_commit_factory() -> requests.Response:
    if not len(user_list) > 0:
        return r_user_factory()
    creator_id = random.choice(user_list)
    return requests.put(COMMIT_URL, json=Commit.fake(creator_id).dump(), headers=HEADER)
