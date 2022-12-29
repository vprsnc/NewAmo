import os
import re

from datetime import datetime
from dateutil import parser

from loguru import logger

from amo.getter import get_entity
from amo.utilities import comprehend_lead_custom_fields

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

    get_entity(
        **arguments, logon_data=franchize,
        code=code if code else None
    )

    # tleads = read_entity(arguments['entity'], arguments['amo'])
    # nleads = tuple(comprehend_lead_custom_fields(lead) for lead in tleads)
    # try:
    #     send_entity(
    #         arguments['entity'],
    #         'franchize', nleads, if_exists='replace'
    #     )
    #     logger.success("ETL process finished successfully, cleaning up...")
    #     open(
    #         f"temp_data/{arguments['amo']}_{arguments['entity']}_tmp.json",
    #         "w"
    #     ).close()
    # except Exception as e:
    #     logger.critical(e)
