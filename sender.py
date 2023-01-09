import os
import pandas as pd

from loguru import logger
from google.cloud import bigquery as bq

from amo.builders import *
from amo.utilities import read_json, timer_decorator

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = \
    './tokens/oddjob-db-2007-759fe782b144.json'
client = bq.Client()


@timer_decorator
def read_entity(entity, amo):
    """Function a tuple of named tuples defined per entity in builders.py"""
    entity_file = open(
        f'temp_data/{amo}_{entity}_tmp.json', 'r',
        encoding='utf-8'
    )

    build_entity = 'build_' + entity + '_tuple'
    yield (
        globals()[build_entity](entry) for entry in tuple(
            read_json(entity_file)
        )
    )


@timer_decorator
def send_entity(entity, amo, records, if_exists):
    """Function uses basic functionality of bigquery python
        library to send JSON to a database.
       If_exists takes following arguments: 'replace', 'append'"""
    df = pd.DataFrame.from_records(records)
    if 'custom_fields_values' in df.columns:
        df.drop('custom_fields_values', axis=1, inplace=True)
    try:
        df.to_gbq(
            f"{amo}_oddjob.dw_amocrm_{entity}", if_exists=if_exists
        )

    except ConnectionAbortedError as excep:
        logger.critical(excep)
