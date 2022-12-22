import os
import re

from datetime import datetime
from dateutil import parser

from loguru import logger
from cyrtranslit import to_latin

from amo.getter import get_entity
from amo.entities import Leads
from amo.utilities import inherit_named_tuple

from setup import franchize_test #TODO replace
from sender import send_entity, read_entity

logger.add(
     'logs/franchize_lead_status_changes.log', backtrace=True, diagnose=True, level='DEBUG'
)

# with open('last_date_franchize_lead_status_changes.txt', 'r') as f:
#     last_date = str(
#         datetime.timestamp(parser.parse(f.read()))
#     ).split('.', maxsplit=1)[0]

last_date = str(datetime.timestamp(parser.parse("2022-12-20"))) #TODO delete

try:
    code = os.environ["CODE"]
except KeyError:
    code = None

arguments = {
    'entity': "leads",
    'amo':  'franchize',
    'filters': f'?filter[created_at][from]={last_date}', #TODO delete last date
    }


tleads = tuple(read_entity(arguments['entity'], arguments['amo']))


def comprehend_custom_fields(lead):
    new_fields = tuple(
        ''.join(
            c for c in to_latin(i['field_name'], lang_code='ru') if c.isalpha() or c.isdigit()
        )
        for i in lead.custom_fields_values
    )
    New_lead = inherit_named_tuple('FrLead', Leads, new_fields)

    ddict = {}
    for i in lead.custom_fields_values:
        dkey = ''.join(c for c in to_latin(i['field_name'], lang_code='ru') if c.isalpha() or c.isdigit())
        dvalue = i['values'][0]['value']
        for k in i['values'][1::]:
            dvalue += f', {k["value"]}'
        ddict[dkey] = dvalue

    new_lead = New_lead(**lead._asdict(), **ddict)

    return new_lead


nleads = tuple(comprehend_custom_fields(lead) for lead in tleads)



# if __name__ == "__main__":

#     logger.info(
#         f"Starting {arguments['entity']} ETL process at {datetime.now()}"
#     )

#     try:
#         get_entity(
#             **arguments, logon_data=franchize,
#             code=(code if code else None)
#         )

#         try:
#             send_entity(
#                 arguments['entity_subtype'],
#                 'franchize', if_exists='append'
#             )
#             logger.success("ETL process finished successfully, cleaning up...")
#             open(
#                 f"temp_data/{arguments['amo']}_{arguments['entity_subtype']}_tmp.json",
#                 "w"
#             ).close()

#         except Exception as e:
#             logger.critical(f"Sedning process failure: {e}")

#     except Exception as e:
#         logger.critical(f"ETL process failure: {e}")
