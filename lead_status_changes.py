import json
from builders import *
from utilities import read_json

from sqlalchemy.engine import create_engine
from sqlalchemy.schema import *


engine = create_engine('bigquery://')


def read_entity(entity):
    entity_file = open(f'{entity}_tmp.json', 'r', encoding='utf-8')
    build_entity = 'build_' + entity + '_tuple'
    return (globals()[build_entity](entry) for entry in tuple(read_json(entity_file)))


def send_entity(entity):


if __name__ == "__main__":

    read_entity1 = read_entity('lead_status_changes')
    print(*read_entity1)
