from exceptions import ApiException
from exceptions import ClientException
import requests
from urlparse import urlparse


class Connection(object):

    def __init__(self, url, **kwargs):
        self.url = urlparse(url)

        if self.url.scheme not in ['http', 'https']:
            raise ClientException(
                u'{} protocol is not supported'.format(self.url.scheme))

        self.user_agent = kwargs.get('user_agent', 'python-json2xlsclient')
        self.timeout = kwargs.get('timeout', 20)
        self.read_timeout = kwargs.get('read_timeout', 20)
        self.verify = bool(kwargs.get('ssl_verify', True))
        retries = kwargs.get('max_retries', 5)

        self.session = requests.Session()

        self.session.mount("https://",
                           requests.adapters.HTTPAdapter(max_retries=retries))
        self.session.mount("http://", requests.adapters.HTTPAdapter(
            requests.adapters.HTTPAdapter(max_retries=retries)))

    def _request(self, *args, **kwargs):
        return self.session.request(*args, **kwargs)

    def request(self, method, path, data=None, files=None, headers=None,
                **extras):
        headers = headers or {}
        headers['user-agent'] = self.user_agent

        if not path.startswith('/'):
            path = u'/{}'.format(path)

        self.last_response = self._request(
            method,
            u'{}://{}{}'.format(self.url.scheme, self.url.netloc, path),
            headers=headers, data=data, files=files, verify=self.verify,
            timeout=(self.timeout, self.read_timeout), **extras)

        if 400 <= self.last_response.status_code < 500:
            raise ClientException(None, self.last_response)

        if not 200 <= self.last_response.status_code < 400:
            raise ApiException(None, self.last_response)

        return self.last_response

    def get(self, path, headers=None, **extras):
        return self.request('GET', path, headers, extras)

    def post(self, url_path, file_path=None, payload=None, headers=None):
        return self._request_with_body(
            'POST', url_path, file_path, payload, headers=None)

    def put(self, url_path, file_path=None, payload=None, **headers):
        return self._request_with_body(
            'PUT', url_path, file_path, payload, headers=None)

    def patch(self, url_path, file_path=None, payload=None, **headers):
        return self._request_with_body(
            'PATCH', url_path, file_path, payload, headers=None)

    def delete(self, url_path, headers=None):
        return self.request('DELETE', url_path)

    def _request_with_body(self, method, url_path, file_path=None,
                           payload=None, headers=None):
        if method not in ['POST', 'PUT']:
            raise ClientException(u'method arg must either be a POST or PUT!')

        if file_path is not None:
            file_data = open(file_path, 'rb')
            fdata = file_data.read()
            file_data.close()

        return self.request(method, url_path, payload, headers, fdata)


class ConnectionSingleton(Connection):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instances:
            cls._instances = super(Connection, cls).__call__(*args, **kwargs)
        return cls._instance