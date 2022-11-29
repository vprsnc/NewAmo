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
    'code': 'def50200249e5ba38f0291199f716fdfc7925a43f925e6c3c5be9b1b897a27221737339ea07e410719babd59a146d29d7c5d2a2bdaaa80dc35b41b52e6128d7946a1aabb3aab5a0e401f8ea3c64b1f49015052159c8f0e2b7481adeb9aa6b15365953bd4343d57368834cb345aa63e207478071451a435f45c36f4cbd96dcef13739133966aeb218d7fc3df14991f5bfe9497c0f0c64f09b693e449c3311da186487137d0c1b9f4e40464ce801de1e3e561afd0529dcd90fffd46f620d1f5bfa0f7d293cfa6f4741bd8340f39e082f203e34ccc3f9051404902310359d1c0c254295d84709e98e809cf6a67b755ffc0071b036b303d52da5f8a1c9138ef632a13179d1e9484b12b9ce26484f28675ce7404e414d2c00ed64e1e5cb1cbc83fc79c61d31b7d0ffdf27b3eed4947832d50d2c2cc1a444411119e3ad8591f909f8cde7730efb3e46d9a8834ad1b39c0c61fd04440f2983f666e7210672d85f0fd6a8b0bfb3b43b37fadb95c2825a91e2d58a985996b65787122f04f1aebb6147f62f3ebbc0aa2865343dadfa1baaab242e1064775297fc8ffbeb5c7dc6f6e0fb5c835b32f435e0d9ed6e79a9fa749fade55b0dcd1183c3a3aebe1142cf9bf2949f5f19f15243f8f0dc51041311c675579f377a2383c802b873ddd28cd30024'
    }


if __name__ == "__main__":

    # logger.info(
    #     f"Starting {arguments['entity']} ETL process at {datetime.now()}"
    # )

    # if get_entity(logon_data=franchize, **arguments):

        if send_entity(arguments['entity'], 'franchize'):
            logger.success("ETL process finished successfully, cleaning up...")
            open(f"temp_data/{arguments['entity']}_tmp.json", "w").close()

        else:
            logger.critical("Sedning process failure")

    # else:
    #     logger.critical("ETL process failure")
