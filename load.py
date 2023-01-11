import os
import pandas as pd

from loguru import logger
from google.cloud import bigquery as bq

from amo.utilities import read_json, timer_decorator


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = \
    './tokens/oddjob-db-2007-759fe782b144.json'
client = bq.Client()


@timer_decorator
def send_entity(entity, amo, if_exists):
    """Function uses basic functionality of bigquery python
        library to send JSON to a database.
       If_exists takes following arguments: 'replace', 'append'"""
    df = pd.read_csv(
        f'temp_data/{amo}_{entity}.csv'
    )
    if 'custom_fields_values' in df.columns:
        df.drop('custom_fields_values', axis=1, inplace=True)
    try:
        df.to_gbq(
            f"{amo}_oddjob.dw_amocrm_{entity}", if_exists=if_exists
        )

        logger.success("ETL process finished successfully, cleaning up...")
        open(
            f"temp_data/{amo}_{entity}_tmp.json",
            "w"
        ).close()
    except ConnectionAbortedError as excep:
        logger.critical(excep)
        return False
