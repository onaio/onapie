import json


class StatsManager(object):

    def __init__(self, conn, stats_path):
        self.conn = conn
        self.stats_ep = stats_path

    def get(self, pk, method=None):
        """Get submitted data for a given form"""
        path = '{}/{}?'.format(self.stats_ep, pk)
        if method is not None:
            path = '{}method={}'.format(path, method)

        return json.loads(self.conn.get(path).text)
