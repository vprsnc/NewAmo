import os
import re

from datetime import datetime
from dateutil import parser

from loguru import logger

from amo.getter import get_entity
from amo.utilities import comprehend_lead_custom_fields, timer_decorator

from setup import franchize
from sender import send_entity, read_entity
from amo.entities import Leads

logger.add(
     'logs/franchize_leads.log', backtrace=True, diagnose=True, level='DEBUG'
)

try:
    code = os.environ["CODE"]
except KeyError:
    code = None

arguments = {
    'entity': "leads",
    'amo':  'franchize',
    }


if __name__ == "__main__":

    logger.info(
        f"Starting {arguments['entity']} ETL process at {datetime.now()}"
    )

    # try:
    #     @timer_decorator
    #     get_entity(
    #         **arguments, logon_data=franchize,
    #         code=code if code else None
    #     )
    # except Exception as e:
    #     logger.critical(f'getting falied with: {e}')


    try:
        tleads = read_entity(arguments['entity'], arguments['amo'])
        nleads = tuple(comprehend_lead_custom_fields(lead) for lead in tleads)
    except Exception as e:
        logger.critical(f'reading falied with: {e}')

    try:
        @timer_decorator
        send_entity(
            arguments['entity'],
            'franchize', nleads, if_exists='replace'
        )
        logger.success("ETL process finished successfully, cleaning up...")
        open(
            f"temp_data/{arguments['amo']}_{arguments['entity']}_tmp.json",
            "w"
        ).close()
    except Exception as e:
        logger.critical(f'sending falied with: {e}')
