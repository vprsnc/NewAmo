import os

from datetime import datetime
from dateutil import parser

from loguru import logger
from amo.getter import get_entity

from setup import franchize
from sender import send_entity, read_entity

logger.add(
     'logs/franchize_calls.log', backtrace=True, diagnose=True, level='DEBUG'
)

with open('last_date_franchize_lead_status_changes.txt', 'r') as f:
    last_date = str(
        datetime.timestamp(parser.parse(f.read()))
    ).split('.', maxsplit=1)[0]

try:
    code = os.environ["CODE"]
except KeyError:
    code = None

arguments = {
    'entity': "leads",
    'amo':  'franchize',
    'filters': f'?notes/filter[type]=call_in', #TODO &filter[created_at][from]={last_date}',
    'entity_subtype': 'notes'
    }


if __name__ == "__main__":

    logger.info(
        f"Starting {arguments['entity']} ETL process at {datetime.now()}"
    )

    get_entity(
        **arguments, logon_data=franchize,
        code=(code if code else None)
    )

    # records = tuple(read_entity(arguments['entity_subtype'], arguments['amo']))
    # send_entity(
    #     arguments['entity_subtype'],
    #     'franchize', records, if_exists='append'
    # )
    # logger.success("ETL process finished successfully, cleaning up...")
    # open(
    #     f"temp_data/{arguments['amo']}_{arguments['entity_subtype']}_tmp.json",
    #     "w"
    # ).close()
