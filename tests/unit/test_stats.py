from onapie.stats import StatsManager
from onapie.utils import ConnectionSingleton
from tests.utils import MockResponse
import json
import mock
import unittest


class StatsMethodsTestCase(unittest.TestCase):

    def setUp(self):
        super(StatsMethodsTestCase, self).setUp()
        self.stats_path = '/some/path'
        self.conn = ConnectionSingleton('http://mock_host')
        self.sm = StatsManager(self.conn, self.stats_path)

    def test_get(self):
        with mock.patch.object(self.sm.conn, 'get',
                               return_value=MockResponse(200, 'Success',
                                                         '{}')) as mock_get:
            self.sm.get('test_pk')
            mock_get.assert_called_with(
                '{}/test_pk?'.format(self.stats_path))

            self.sm.get('test_pk','methodX')
            mock_get.assert_called_with(
                '{}/test_pk?method=methodX'.format(self.stats_path))
