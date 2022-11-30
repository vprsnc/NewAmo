from datetime import datetime
from dateutil import parser

from loguru import logger
from amo.getter import get_entity

from setup import franchize
from sender import send_entity

logger.add(
     'out.log', backtrace=True, diagnose=True, level='DEBUG'
)

with open('lead_status_changes_last_date.txt', 'r') as f:
    last_date = str(
        datetime.timestamp(parser.parse(f.read()))
    ).split('.')[0]


arguments = {
    'entity': "lead_status_changes",
    'tokens_folder':  'tokens/franchize',
    'filters': f'?filter[type]=lead_status_changed&filter[updated_at][from]={last_date}',
    }


if __name__ == "__main__":

    logger.info(
        f"Starting {arguments['entity']} ETL process at {datetime.now()}"
    )

    if get_entity(logon_data=franchize, **arguments):

        if send_entity(arguments['entity'], 'franchize', if_exists='append'):
            logger.success("ETL process finished successfully, cleaning up...")
            open(f"temp_data/{arguments['entity']}_tmp.json", "w").close()

        else:
            logger.critical("Sedning process failure")

    else:
        logger.critical("ETL process failure")
