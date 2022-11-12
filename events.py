import requests
from setup import franchize
from logon import build_header

if __name__ == '__main__':

    r = requests.get(
        f'https://{franchize.subdomain}.amocrm.ru/api/v4/events',
        headers=build_header(franchize, 'tokens/franchize')
       )

    events_dict = json.loads(r.text)
    print(events_dict['_page'])
