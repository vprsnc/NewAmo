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
    'code': "def50200edbb57cfb1caac9893a2c5d8a8a1571287b68dfa064641fa2023c1c21108fe6dfeca71d91a5eed9745935bd4d09f2e82650f30064097e0200d96e28ad70857c29ea5ce77492ca1f6f361d90b12f03b09ced3041cdd59997348661b5390eda598b2dbc8949d238a51fae5670eee538126a9860f6a6dbf118fdeb330cc35faac409903db73403ee74b72b4e3fdccd0053008f9d9c3502af279918e93506401a7f0a0ae21fe57b13750d3e04555db85d7f367f6a4b0323db18140d04bb1a1dff07eca393169056ce904785ffaf3bda3a564e3688012064585d2039b7c5487359a60ccec783b1136c4e37e3d085b92c16fe309f6495ee100d0e3e5cb599a68b525f06f4a94b350e32fd6714070653fe4af61c6a0766b25f5e850b45066f8a75eb8c53177b4c0f1e8fd51bbc29c7594e58cbbcf0af016e59504daf457092bf36f6ac3a5d04faf3fba3c47024eb2489cfe905833e1ffa1e4e35787dd494da3c39a0384d0df9b79e771320c9c4cac5c71089ccce814bb62d93bc3e4048e5b8562b2e2d1aff11645e7f4ec24ae958a673b7b527dc34e69b1f088f7466367ad410cdb12d86956acae436a3a6e0ad21cf3d76405aa110633bc9a623141a35a31089f008cb26f57b67339b59c204b479d1f6fff47901d44c56cb926a9f52c"
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
