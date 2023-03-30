from models import User, Commit
import time
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

# Set the API endpoint URL and the data to send
API_URL = 'http://127.0.0.1:5000'
USER_URL = f'{API_URL}/user'
COMMIT_URL = f'{API_URL}/commit'

# Set the API key as a header
HEADER = {'x-access-token': 'dev'}

r_user_factory = lambda: requests.put(USER_URL, json=User.fake().__dict__, headers=HEADER)
r_commit_factory = lambda creator_id: requests.put(COMMIT_URL, json=Commit.fake(creator_id).__dict__, headers=HEADER)

def main():
    print("Sending user data...")
    for _ in range(10):
        response: requests.Response = r_user_factory()
        check_error(response)

    print("Sending commit data...")
    for _ in range(10):
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
            if random.random() > 0.1:
                response: requests.Response = r_commit_factory(creator_id=user_id)
                print("Commit created")
            else:
                response: requests.Response = r_user_factory()
                print("User created")
        check_error(response)   
        time.sleep(2)

if __name__ == "__main__":
    while True:
        try:
            main()
        except requests.ConnectionError:
            print("Connection error")
            time.sleep(5)
        except requests.Timeout:
            print("Timeout")
            time.sleep(5)
        except requests.HTTPError:
            print("HTTP error")
            break
        except requests.TooManyRedirects:
            print("Too many redirects")
            break