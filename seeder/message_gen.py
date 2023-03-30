from seeder.messages import messages
import itertools
import random


class MessageGen:
    def __init__(self):
        self.lst = messages
        random.shuffle(self.lst)
        self.cycle = itertools.cycle(self.lst)
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            item = next(self.cycle)
            self.index += 1
            return item
        except StopIteration:
            random.shuffle(self.lst)
            self.cycle = itertools.cycle(self.lst)
            self.index = 0
            item = next(self.cycle)
            self.index += 1
            return item


gen = MessageGen()
