from onapie.exceptions import ApiException, ClientException
from tests.utils import MockResponse
import unittest


class ExceptionsTestCase(unittest.TestCase):

    def test_plain_exception_messeges(self):
        msglist = [str(ApiException('Test Message')),
                   str(ClientException('Test Message')),
                   'Test Message']
        self.assertTrue(msglist[1:] == msglist[:-1], 
                        u'Basic exception messages fail to print as expected.')

    def test_http_exception_messeges(self):
        resp = MockResponse(404, 'Not Found', '{"detail": "Not found"}')

        msglist = [str(ApiException(None, resp)),
                   str(ClientException(None, resp)),
                   '404, Not Found']

        self.assertTrue(msglist[1:] == msglist[:-1], 
                        u'HTTP exception messages fail to print as expected.')
