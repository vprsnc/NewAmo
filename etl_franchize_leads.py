import os
import re
import csv

from datetime import datetime
from dateutil import parser

from loguru import logger

from amo.getter import get_entity
from amo.utilities import comprehend_lead_custom_fields, timer_decorator

from setup import franchize
from load import send_entity
from amo.entities import Leads
from transform import transform_entity

logger.add(
     'logs/franchize_leads.log', backtrace=True, diagnose=True, level='DEBUG'
)

try:
    code = os.environ["CODE"]
except KeyError:
    code = None

with open('last_date_franchize_leads.txt', 'r') as f:
    last_date = str(
       datetime.timestamp(parser.parse(f.read()))
   ).split('.', maxsplit=1)[0]

arguments = {
    'entity': "leads",
    'amo':  'franchize',
    'filters': f'?notes/filter[created_at][from]={last_date}',
    }


if __name__ == "__main__":
    logger.info(
        f"Starting {arguments['entity']} ETL process at {datetime.now()}"
    )

    # Extract:
    get_entity(
        **arguments, logon_data=franchize,
        code=code if code else None
    )

    # Transform:
    transform_entity('leads', 'franchize')

    # Load:
    send_entity(
        arguments['entity'],
        'franchize', if_exists='append'
    )
