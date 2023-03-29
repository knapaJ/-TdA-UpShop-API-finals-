from dataclasses import dataclass
import time
import requests
import faker
import random

@dataclass(init=True, repr=True)
class User:
    name: str
    surname: str
    nick: str
    avatar_url: str

@dataclass(init=True, repr=True)
class Commit:
    creator_id: str
    date: str | None = None
    lines_added: int = 0
    lines_removed: int = 0
    description: str = ""

def check_error(response: requests.Response):
    if not response.ok:
        print(f"Error: {response.status_code} {response.reason}")
        raise Exception(response.reason)

fake = faker.Faker()

def user_factory():
    return User(
        nick=fake.user_name(),
        name=fake.first_name(),
        surname=fake.last_name(),
        avatar_url=f"https://picsum.photos/seed/{fake.uuid4()}/200/200"
        )

def get_random_user_id()->str|None:
    response: requests.Response = requests.get(USER_URL, headers=HEADER)
    check_error(response)
    users = response.json()
    if not users:
        return None
    return random.choice(users)['userID']

def commit_factory(creator_id: str):
    return Commit(
        creator_id=creator_id,
        date=fake.date_time_between(start_date="-1y", end_date="now").isoformat(),
        lines_added=random.randint(0, 100),
        lines_removed=random.randint(0, 100),
        description=fake.text(max_nb_chars=20)
        )

# Set the API endpoint URL and the data to send
API_URL = 'http://127.0.0.1:5000'
USER_URL = f'{API_URL}/user'
COMMIT_URL = f'{API_URL}/commit'

# Set the API key as a header
HEADER = {'x-access-token': 'dev'}

r_user_factory = lambda: requests.put(USER_URL, json=user_factory().__dict__, headers=HEADER)
r_commit_factory = lambda creator_id: requests.put(COMMIT_URL, json=commit_factory(creator_id).__dict__, headers=HEADER)

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