from onapie.xlsforms import XlsFormsManager
from onapie.exceptions import ClientException
from onapie.utils import ConnectionSingleton
from tests.utils import MockResponse
import mock
import unittest
from random import choice


mock_http_call = mock.Mock()
mock_http_call.return_value = MockResponse(200, 'OK', '{}')
mock_del_204_http_call = mock.Mock()
mock_del_204_http_call.return_value = MockResponse(204, 'Deleted', '{}')


@mock.patch.multiple(ConnectionSingleton,
                     get=mock_http_call,
                     post=mock_http_call,
                     put=mock_http_call,
                     patch=mock_http_call,
                     delete=mock_del_204_http_call)
class XlsFormsManagerTestCase(unittest.TestCase):

    def setUp(self):
        super(XlsFormsManagerTestCase, self).setUp()
        self.path = '/some/path'
        self.conn = ConnectionSingleton('http://mock_host')
        self.xlsmgr = XlsFormsManager(self.conn, self.path)

    def test_create_mutually_exclusive_args(self):
        with self.assertRaises(ClientException):
            self.xlsmgr.create()

        with self.assertRaises(ClientException):
            self.xlsmgr.create('xls_path', 'xls_url')

    def test_create_from_file_call(self):
        self.xlsmgr.create('xls_path')
        self.conn.post.assert_called_with(self.path, 'xls_path', None)

    def test_create_from_url_call(self):
        self.xlsmgr.create(None, 'xls_url')
        self.conn.post.assert_called_with(self.path, None, 'xls_url')

    def test_list_call(self):
        self.xlsmgr.list()
        self.conn.get.assert_called_with(self.path)

    def test_list_owner_call(self):
        self.xlsmgr.list('ownerX')
        self.conn.get.assert_called_with('{}?owner=ownerX'.format(self.path))

    def test_get_form_call(self):
        self.xlsmgr.get('pk')
        self.conn.get.assert_called_with('{}/pk'.format(self.path))

    def test_get_form_invalid_representation_exception(self):
        with self.assertRaises(ClientException):
            self.xlsmgr.get('pk', 'invalid_repr')

    def test_get_form_representation_call(self):
        rep = choice(['json', 'xml', 'xls'])
        self.xlsmgr.get('pk', rep)
        self.conn.get.assert_called_with(
            '{}/pk/form.{}'.format(self.path, rep))

    def test_get_form_with_tags_call(self):
        self.xlsmgr.get('pk', None, 'foo1', 'bar1', 'foo2', 'bar2')
        self.conn.get.assert_called_with(
            '{}/pk?tags=foo1,bar1,foo2,bar2'.format(self.path))

    def test_get_form_representation_with_tags_call(self):
        rep = choice(['json', 'xml', 'xls'])
        self.xlsmgr.get('pk', rep, 'foo1', 'bar1', 'foo2', 'bar2')
        self.conn.get.assert_called_with(
            '{}/pk/form.{}?tags=foo1,bar1,foo2,bar2'.format(self.path, rep))

    def test_update_form_call(self):
        self.xlsmgr.update('pk', 'uuid', 'desc', 'owner', 'pub', 'dat')
        self.conn.put.assert_called_with('{}/pk'.format(self.path), None,
                                         ('uuid=uuid&description=desc'
                                          '&owner=owner&public=pub'
                                          '&public_data=dat'))

    def test_patch_form_call(self):
        self.xlsmgr.patch('pk', foo1='bar1', foo2='bar2')
        self.conn.patch.assert_called_with('{}/pk'.format(self.path),
                                           None, 'foo1=bar1&foo2=bar2')

    def test_delete_response_exception(self):
        with mock.patch.object(ConnectionSingleton, 'delete', mock_http_call):
            with self.assertRaises(ClientException):
                self.xlsmgr.delete('pk')

    def test_delete(self):
        self.xlsmgr.delete('pk')
        self.conn.delete.assert_called_with('{}/pk'.format(self.path))
