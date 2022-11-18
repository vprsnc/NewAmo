from collections import namedtuple


Logon_data = namedtuple(
    'Logon_data',
    ['client_id', 'client_secret', 'subdomain', 'redirect_uri']
)

Event = namedtuple(
    'Event',
    ['id', 'type', 'entity_id', 'entity_type', 'created_by',
     'created_at', 'value_after', 'value_before', 'account_id']
)
