from models import User, Commit
from config import *
import requests
import random

def check_error(response: requests.Response):
    if not response.ok:
        print(f"Error: {response.status_code} {response.reason}")
        raise Exception(response.reason)

def get_random_user_id()->str|None:
    response: requests.Response = requests.get(USER_URL, headers=HEADER)
    check_error(response)
    users = response.json()
    if not users:
        return None
    return random.choice(users)['userID']

r_user_factory = lambda: requests.put(USER_URL, json=User.fake().__dict__, headers=HEADER)
r_commit_factory = lambda creator_id: requests.put(COMMIT_URL, json=Commit.fake(creator_id).__dict__, headers=HEADER)
