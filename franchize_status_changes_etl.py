from datetime import datetime

from loguru import logger
from amo.getter import get_entity

from setup import franchize
from sender import send_entity

logger.add(
     'out.log', backtrace=True, diagnose=True, level='DEBUG'
)

arguments = {
    'entity': "lead_status_changes",
    'tokens_folder':  'tokens/franchize',
    'filters': '?filter[type]=lead_status_changed'
    }


if __name__ == "__main__":
    logger.info(
        f"Starting {arguments['entity']} ETL process at {datetime.now()}"
    )
    get_entity(logon_data=franchize, **arguments)
    if send_entity(arguments['entity'], 'franchize'):
        logger.success("ETL process finished successfully, cleaning up...")
        open(f"{arguments['entity']}_tmp.json", "w").close()
    else:
        logger.critical("ETL process failure")
