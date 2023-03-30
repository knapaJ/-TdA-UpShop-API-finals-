from dataclasses import dataclass
from seeder.message_gen import gen
import faker
import random

fake = faker.Faker(['cs_CZ'])


@dataclass(init=True, repr=True)
class User:
    name: str
    surname: str
    nick: str

    @staticmethod
    def fake():
        return User(
            nick=fake.user_name(),
            name=fake.first_name(),
            surname=fake.last_name()
        )

    def dump(self):
        ret = {}
        for (key, value) in self.__dict__.items():
            if value:
                ret[key] = value
        return ret


init = True


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
            date=fake.date_time_between(start_date="-1y", end_date="now").isoformat() if init else None,
            lines_added=random.randint(0, 100),
            lines_removed=random.randint(0, 100),
            description=gen.__next__()  # fake.text(max_nb_chars=300)
        )

    def dump(self):
        ret = {}
        for (key, value) in self.__dict__.items():
            if value is not None:
                ret[key] = value
        return ret
