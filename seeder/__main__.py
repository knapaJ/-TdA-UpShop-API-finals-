from config import *
from utils import *
import time
import requests
import random

def main():
    print("Sending user data...")
    for _ in range(START_USERS):
        response: requests.Response = r_user_factory()
        check_error(response)

    print("Sending commit data...")
    for _ in range(START_COMMITS):
        user_id = get_random_user_id()
        response: requests.Response = r_commit_factory(creator_id=user_id)
        check_error(response)
        
    print("Sending data in a loop...")
    # Send the data in a loop

    while True:
        # Get user ID
        user_id = get_random_user_id()

        if user_id is None:
            response: requests.Response = r_user_factory()
            print("No users in database, user created")
        else:
            if random.random() > USER_PROPORTION:
                response: requests.Response = r_commit_factory(creator_id=user_id)
                print("Commit created")
            else:
                response: requests.Response = r_user_factory()
                print("User created")
        check_error(response)   
        time.sleep(REQUEST_DELAY)

if __name__ == "__main__":
    while True:
        try:
            main()
        except requests.ConnectionError:
            print("Connection error")
            time.sleep(CONNECTION_DELAY)
        except requests.Timeout:
            print("Timeout")
            time.sleep(TIMEOUT_DELAY)
        except requests.HTTPError:
            print("HTTP error")
            break
        except requests.TooManyRedirects:
            print("Too many redirects")
            break