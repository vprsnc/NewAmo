import requests
from collections import namedtuple
from pathlib import Path
import json
from pprint import pprint


Logon_data = namedtuple(
    'Logon_data',
    ['client_secret', 'client_id', 'subdomain', 'redirect_uri']
)


# Temporary @TODO: delete me!

franchize = Logon_data(
    client_secret='fy7dA4ouR4uLcW98JHb2EadFJwYYvKb0mXauxtN9A0POFKsJCJNoh0puPALc2qNn',
    client_id='6a15b109-a8b4-4345-ba0d-249544d84acb',
    subdomain='yastaff',
    redirect_uri='https://yastaff.amocrm.ru/amo'
)

def read_token(tokens_folder, token_type):
    try:
        access_token = Path(f"./{tokens_folder}/{token_type}_token.txt").read_text()
        return access_token
    except FileNotFoundError:
        return None


def token_is_fresh(header, subdomain):
    if requests.get(
        f'https://{subdomain}.amocrm.ru/api/v4/account',
        headers=header
    ).status_code == 200:
        return True
    else:
        return False


def get_token(logon_data, tokens_folder, code=None):
    new_url = f'https://{logon_data.subdomain}.amocrm.ru/oauth2/access_token'

    if read_token(tokens_folder, 'refresh'):
        data = namedtuple('data', logon_data._fields + ('grant_type', 'refresh_token'))
        login_data = data(*logon_data, grant_type='refresh_token', refresh_token=read_token(tokens_folder, 'refresh'))

        request = requests.post(new_url, data=login_data._asdict())
        request_dict = json.loads(request.text)

        with open(f'{tokens_folder}/refresh_token.txt', 'w') as file:
            file.write(request_dict[f"refresh_token"])

    elif code:
        data = namedtuple('data', logon_data._fields + ('grant_type', 'code'))
        login_data = data(*logon_data, grant_type='authorization_code', code=code)

        pprint(login_data._asdict())
        request = requests.post(new_url, data=login_data._asdict())
        request_dict = json.loads(request.text)

        pprint(request_dict)
        for token in ['refresh', 'access']:
            with open(f'{tokens_folder}/{token}_token.txt', 'w') as file:
                file.write(request_dict[f"{token}_token"])

    else:
        print('you need to provide and authorization code/refresh token')


def build_header(logon_data, tokens_folder, code=None):
    if read_token(tokens_folder, 'access') is not None:
        if token_is_fresh(
    header={'Authorization': 'Bearer ' + read_token('tokens/franchize', 'access')},
    subdomain=franchize.subdomain
):
            return {'Authorization': 'Bearer ' + read_token(tokens_folder, 'access')}
        else:
            get_token(logon_data, tokens_folder)
            return build_header(logon_data, tokens_folder)
    else:
        get_token(logon_data, tokens_folder, code)
        return build_header(logon_data, tokens_folder)


