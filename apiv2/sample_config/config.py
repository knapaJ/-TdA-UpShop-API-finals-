# THIS IS SAMPLE CONFIG
import os
from random import randbytes
import csv

SECRET_KEY = randbytes(30)
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(os.path.dirname(__file__), "app.db")
RESTX_MASK_SWAGGER = False

K_MASTER_TOKEN = "edit this"

K_CONTRACTOR_TOKEN_LIST = {}

with open(os.path.join(os.path.dirname(__file__), 'hashes.secret')) as secret:
    for line in csv.reader(secret):
        print(f"Loaded hash [{line[2]}] of team '{line[1]}'")
        K_CONTRACTOR_TOKEN_LIST[line[2]] = line[1]
