from datetime import datetime
from dateutil import parser

from loguru import logger
from amo.getter import get_entity

from setup import franchize
from sender import send_entity

logger.add(
     'logs/franchize_lead_status_changes.log', backtrace=True, diagnose=True, level='DEBUG'
)

with open('franchize_lead_status_changes_last_date.txt', 'r') as f:
    last_date = str(
        datetime.timestamp(parser.parse(f.read()))
    ).split('.', maxsplit=1)[0]


arguments = {
    'entity': "lead_status_changes",
    'amo':  'franchize',
    'filters': f'?filter[type]=lead_status_changed&filter[created_at][from]={last_date}',
    }


if __name__ == "__main__":

    logger.info(
        f"Starting {arguments['entity']} ETL process at {datetime.now()}"
    )

    try:
        get_entity(logon_data=franchize, **arguments)

        try:
            send_entity(arguments['entity'], 'franchize', if_exists='append')
            logger.success("ETL process finished successfully, cleaning up...")
            open(f"temp_data/{arguments['entity']}_tmp.json", "w").close()

        except Exception as e:
            logger.critical(f"Sedning process failure: {e}")

    except Exception as e:
        logger.critical(f"ETL process failure: {e}")
