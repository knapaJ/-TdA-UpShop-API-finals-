from dataclasses import dataclass
import faker
import random

fake = faker.Faker()

@dataclass(init=True, repr=True)
class User:
    name: str
    surname: str
    nick: str
    avatar_url: str

    @staticmethod
    def fake():
        return User(
            nick=fake.user_name(),
            name=fake.first_name(),
            surname=fake.last_name(),
            avatar_url=f"https://picsum.photos/seed/{fake.uuid4()}/200/200"
        )

@dataclass(init=True, repr=True)
class Commit:
    creator_id: str
    date: str | None = None
    lines_added: int = 0
    lines_removed: int = 0
    description: str = ""

    @staticmethod
    def fake(creator_id):
        return Commit(
            creator_id=creator_id,
            date=fake.date_time_between(start_date="-1y", end_date="now").isoformat(),
            lines_added=random.randint(0, 100),
            lines_removed=random.randint(0, 100),
            description=fake.text(max_nb_chars=20)
        )
