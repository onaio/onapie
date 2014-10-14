import json
from onapie.xlsforms import XlsFormsManager
from onapie.utils import ConnectionSingleton


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

        self.forms = XlsFormsManager(self.conn, self.api_entrypoint)

    def authenticate(self, username, password):
        self.token_key = json.loads(self.conn.get(self.auth_path, None,
                                    auth=(username,
                                          password)).text).get('api_token')
        self.set_token_key(self.token_key)
        return self.token_key

    def set_token_key(self, token_key):
        self.conn.set_header('Authorization', 'Token {}'.format(token_key))
