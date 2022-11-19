import requests
import json

from datetime import datetime
from collections import namedtuple

from pprint import pprint
from loguru import logger

from setup import franchize
from logon import build_session


logger.add(
     'out.log', backtrace=True, diagnose=True, level='DEBUG'
)


def timer_decorator(func):

     def timer():
         start = datetime.now()
         logger.info(f'Starting timer at {start}')
         func()
         end = datetime.now()
         logger.success(f'Ending timer at{end}, it took {end-start}.')

     return timer


def build_url(logon_data, entity, filters=None):
     url = f'https://{logon_data.subdomain}.amocrm.ru/api/v4/{entity}'
     return url + filters if filters else url


def request_entities(url, session):
    request = session.get(url)
    if request.status_code == 200:
        return request
    else:
        logger.critical(f'Something is wrong here!: {r.text}')
        return False


def build_contents(r, entity):
     return json.loads(r.text)['_embedded'][f'{entity}']


def build_next(r):
    try:
        return json.loads(r.text)['_links']['next']['href']
    except KeyError:
        return False


def write_contents(entity, contents):
    for c in contents:
         with open(f'{entity}_tmp.json', 'a', encoding='utf-8') as file:
              json.dump(c, file, indent=4)
              file.write(',\n')

              
def get_entity(entity, logon_data, tokens_folder, filters=None):

    session = build_session(logon_data, tokens_folder) 
    r = request_entities(
         url=build_url(logon_data, entity, filters if filter else None),
         session=session
    )

    write_contents(entity, build_contents(r, entity))

    next_url = build_next(r)

    while True:
        if next_url:
             r = request_entities(next_url, session)
             write_contents(entity, build_contents(r, entity))
             next_url = build_next(r)
        else:
            break

 
if __name__ == '__main__':
    url = f'https://{franchize.subdomain}.amocrm.ru/api/v4/events'
    filters = '?filter[type]=lead_status_changed,lead_added,lead_deleted,lead_restored&filter[created_at][from]=20220101'
    entity = 'events'
    tokens_folder='tokens/franchize'

    timer_decorator(get_entity(entity, franchize, tokens_folder, filters=filters))
    # pprint(json.loads(r.text)['_links']['next']['href'])

    # with open('events_tmp.json', 'r', encoding='utf-8') as file:
    #     # data = list(json.loads(x) for x in file)
    #     data = json.loads('[' + file.read()[:-2] + ']')


    
