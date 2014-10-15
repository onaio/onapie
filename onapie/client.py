import json
from onapie.xlsforms import XlsFormsManager
from onapie.data import DataManager
from onapie.stats import StatsManager
from onapie.utils import ConnectionSingleton
from urlparse import urlparse


class Client(object):

    def __init__(self, api_addr, **kwargs):
        self.api_addr = api_addr
        username = kwargs.get('username', None)
        password = kwargs.get('password', None)
        self.token_key = kwargs.get('token_key', None)
        self.api_entrypoint = kwargs.get('api_entrypoint', '/api/v1')
        auth_path = kwargs.get('auth_path', '/user')
        self.auth_path = '{}{}'.format(self.api_entrypoint, auth_path)

        self.conn = ConnectionSingleton(self.api_addr, **kwargs)

        if all((username, password, not self.token_key)):
            self.authenticate(username, password)

        if kwargs.get('fetch_catalog', True):
            self.fetch_catalog()

    def fetch_catalog(self):
        self.catalog = json.loads(self.conn.get(self.api_entrypoint).text)

        self.forms = XlsFormsManager(
            self.conn, urlparse(self.catalog.get('forms')).path)
        self.data = DataManager(
            self.conn, urlparse(self.catalog.get('data')).path)
        self.stats = StatsManager(
            self.conn, urlparse(self.catalog.get('stats')).path)

    def authenticate(self, username, password):
        self.token_key = json.loads(
            self.conn.get(self.auth_path, None,
                          auth=(username, password)).text).get('api_token')
        self.set_token_key(self.token_key)
        return self.token_key

    def set_token_key(self, token_key):
        self.conn.set_header('Authorization', 'Token {}'.format(token_key))
