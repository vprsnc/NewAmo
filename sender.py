import os
import json
from builders import *
from utilities import read_json


from pprint import pprint


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'tokens/yet-another-python-c9430ad455a2.json'


def read_entity(entity):
    entity_file = open(f'{entity}_tmp.json', 'r', encoding='utf-8')
    build_entity = 'build_' + entity + '_tuple'
    return (
        globals()[build_entity](entry) for entry in tuple(read_json(entity_file))
    )


def send_entity(entity):
    pass


if __name__ == "__main__":
    read_entity1 = read_entity('lead_status_changes')
    pprint(tuple(i._asdict() for i in read_entity1))
