import os
import pandas as pd

from loguru import logger
from google.cloud import bigquery as bq

from amo.builders import *
from amo.utilities import read_json

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = \
    'tokens/oddjob-db-2007-759fe782b144.json'
client = bq.Client()


def read_entity(entity):
    """Function a tuple of named tuples defined per entity in builders.py"""
    entity_file = open(f'{entity}_tmp.json', 'r', encoding='utf-8')
    build_entity = 'build_' + entity + '_tuple'
    return (
        globals()[build_entity](entry) for entry in tuple(
            read_json(entity_file)
        )
    )


def send_entity(entity, amo):
    """Function uses basic functionality of bigquery python
        library to send JSON to a database."""
    try:
        pd.DataFrame.from_records(
            [i._asdict() for i in read_entity(entity)]
        ).to_gbq(
            f"{amo}_oddjob.dw_amocrm_{entity}", if_exists="replace"
        )
        return True
    except ConnectionAbortedError as excep:
        logger.critical(excep)
        return False
