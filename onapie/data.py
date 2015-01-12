import json


class DataManager(object):

    def __init__(self, conn, api_entrypoint):
        self.conn = conn
        self.data_ep = api_entrypoint

    def list_endpoints(self, owner=None):
        """Returns a list of data endpoints

        .. attribute:: owner

            Optional. Get endpoints by owner username
            Pass 'public to get public endpoints'
        """
        query = self.data_ep

        if owner is not None:
            query = '{}?owner={}'.format(query, owner)

        return json.loads(self.conn.get(query).text)

    def get(self, pk, dataid=None, tags=None, query=None,
            sort=None, start=None, limit=None):
        """Get submitted data for a given form"""
        path = '{}/{}'.format(self.data_ep, pk)
        if dataid is not None:
            path = '{}/{}'.format(path, dataid)
        params_format = '{}={}'
        params = []
        if query:
            params.append(params_format.format('query', json.dumps(query)))
        elif tags:
            params.append(params_format.format('tags', ','.join(tags)))
        if(start):
            params.append(params_format.format('start', start))
        if(limit):
            params.append(params_format.format('limit', limit))
        if(sort):
            params.append(params_format.format('sort', json.dumps(sort)))

        if(params):
            path = '{}?{}'.format(path, '&'.join(params))
        return json.loads(self.conn.get(path).text)

    def delete_tag(self, pk, data_id, tag_name):
        return json.loads(
            self.conn.delete('{}/{}/{}/labels/{}'.format(
                self.data_ep, pk, data_id, tag_name)).text)

    def get_enketo_editlink(self, pk, dataid, return_url):
        return json.loads(self.conn.get(
            '{}/{}/{}/enketo?return_url={}'.format(
                self.data_ep, pk, dataid, return_url)).text)
