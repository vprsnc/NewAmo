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
    'code': "def502000a6463ad1a4812c375787bee4f94316dba17d33ea576e625e0f38d77c6b666f0d4bf4aeaa39895be543a5d04544ed99ff72830bccad699f8db65cc118746d6184368134349bd63851b808c6682fa34458b443dbce72b83bebd57fdd2d31dc46e3f5fce74e3f1617a4fd9a7b63ff50453aa57e01a34f8a5fb4924494d291a0770535dea4434e839f9d6d0269e7fb925934300c9d85439900bd7d33e291fcc8952fe3cbf61f31a230d821a342ef1effb953f8bc178c9a34268510b7eff8df9a38da20ea0ea1927dcf496dd7ff3cff844ea0f73efb3704c9c376e21c68a4791df443335aa77b35ee776f70c5c54b26f2ad422c0c2cf01571fe97022657fb0c58ec96e7ebfb0a6d31c6db4a579e879ad6d2e76cd3e7777fd74d22edf0f08c524dc91e8cc71a42ebdc4314f9f7c77d18f820c8effa02d2ae58fcd89260aab99919d7da8982644636b93d2b152c9ba8176c250a233c1dd545a3029bcfae50a8d689e1229d3a3c11efd190043cd3b1a6919c6976271ec24f88b041132198f5d95dd770d85eea0cf1a1fbcb5b6bbf80ad977d657b47718acfec64f6164292e452827574159313c232d6977b8818493782df3d02be16c296dd4f0b2b5a17b260f2862848ce1ce01e66abd5d09cbcaaa4449127d4ed441a4781b786c5e07"
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
