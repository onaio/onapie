from onapie.data import DataManager
from onapie.utils import ConnectionSingleton
from tests.utils import MockResponse
import mock
import unittest


mock_http_call = mock.Mock()
mock_http_call.return_value = MockResponse(200, 'OK', '{}')


@mock.patch.multiple(ConnectionSingleton,
                     get=mock_http_call,
                     delete=mock_http_call)
class DataManagerTestCase(unittest.TestCase):

    def setUp(self):
        super(DataManagerTestCase, self).setUp()
        self.path = '/some/path'
        self.conn = ConnectionSingleton('http://mock_host')
        self.datamgr = DataManager(self.conn, self.path)

    def test_list_all_endpoints_call(self):
        self.datamgr.list_endpoints()
        self.conn.get.assert_called_with(self.path)

    def test_list_owner_endpoints_call(self):
        self.datamgr.list_endpoints('owner')
        self.conn.get.assert_called_with('{}?owner=owner'.format(self.path))

    def test_get_data_by_pk_call(self):
        self.datamgr.get('pk')
        self.conn.get.assert_called_with('{}/pk'.format(self.path))

    def test_get_datum_call(self):
        self.datamgr.get('pk', 'datum_id')
        self.conn.get.assert_called_with('{}/pk/datum_id'.format(self.path))

    def test_get_data_by_query_call(self):
        self.datamgr.get('pk', None, foo1='bar1', foo2='bar2')
        self.conn.get.assert_called_with(
            '%s/pk?query={"foo1": "bar1", "foo2": "bar2"}' % (self.path))

    def test_get_data_by_tag_call(self):
        self.datamgr.get('pk', None, 'foo1', 'bar1', 'foo2', 'bar2')
        self.conn.get.assert_called_with(
            '{}/pk?tags=foo1,bar1,foo2,bar2'.format(self.path))

    def test_delete_data_tag_call(self):
        self.datamgr.delete_tag('pk', 'data_id', 'tag')
        self.conn.delete.assert_called_with(
            '{}/pk/data_id/labels/tag'.format(self.path))

    def test_get_enketo_editlink_call(self):
        self.datamgr.get_enketo_editlink('pk', 'dataid')
        self.conn.delete.assert_called_with(
            '{}/pk/dataid/enketo'.format(self.path))
