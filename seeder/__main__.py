from seeder.handlers import *
from seeder.utils import *
import seeder.models as models
import time
import requests
import random


def main():
    models.init = True
    print("Sending user data...")
    for _ in range(START_USERS):
        response: requests.Response = r_user_factory()
        response.raise_for_status()

    print("Sending commit data...")
    for _ in range(START_COMMITS):
        response: requests.Response = r_commit_factory()
        response.raise_for_status()

    models.init = False
    print("Sending data in a loop...")
    # Send the data in a loop

    while True:
        if random.random() > USER_PROPORTION:
            print("Creating commit...", end=" ")
            response: requests.Response = r_commit_factory()
            response.raise_for_status()
            print("DONE")
        else:
            print("Creating user...", end=" ")
            response: requests.Response = r_user_factory()
            response.raise_for_status()
            print("DONE")

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
        except requests.HTTPError as e:
            response_code = e.response.status_code
            handler = {
                400: handle_400,
                404: handle_404,
                500: handle_500
            }
            handler[response_code](e)
        except requests.TooManyRedirects:
            print("Too many redirects")
            break
