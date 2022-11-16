import requests
import json
from collections import namedtuple

from pprint import pprint
from loguru import logger

from setup import franchize
from logon import build_header


logger.add(
    'out.log', backtrace=True, diagnose=True 
)

Event = namedtuple(
    'Event',
    ['id', 'type', 'entity_id', 'entity_type', 'created_by',
     'created_at', 'value_after', 'value_before', 'account_id']
)


def store_events(events):
    pass 


def parse_events(r):
       # events = (
       #     Event(
       #         id = e['id'],
       #         type = e['type'],
       #         entity_id = e['entity_id'],
               
       #     )e\
       #           for e in r.text['_embedded']['events']events
       # )
        
    pass
    

def write_entities(entity, contents):
    for c in contents:
         with open(f'{entity}_tmp.json', 'a', encoding='utf-8') as file:
              json.dump(c, file, indent=4)
              file.write(',\n')

              
def request_entities(url, headers):
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        return r
    else:
        pprint(r.text)
        return False

if __name__ == '__main__':
    # url = f'https://{franchize.subdomain}.amocrm.ru/api/v4/events?filter[type]=lead_status_changed,lead_added,lead_deleted,lead_restored'
    filters = ''
    entity = 'leads'
    url = f'https://{franchize.subdomain}.amocrm.ru/api/v4/{entity}' + filters
    
    r = request_entities(url, headers=build_header(franchize, 'tokens/franchize'))

    contents = json.loads(r.text)['_embedded'][f'{entity}'] #TODO does it the same for all entities?
    pprint(contents)
    # pprint(json.loads(r.text)['_links']['next']['href'])

    # with open('events_tmp.json', 'r', encoding='utf-8') as file:
    #     # data = list(json.loads(x) for x in file)
    #     data = json.loads('[' + file.read()[:-2] + ']')

            
