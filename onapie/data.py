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

    def get(self, pk, dataid=None, *tag_args, **query_kwargs):
        """Get submitted data for a given form"""
        path = '{}/{}'.format(self.data_ep, pk)
        if dataid is not None:
            path = '{}/{}'.format(path, dataid)
        elif any(query_kwargs):
            path = '{}?query={}'.format(path, json.dumps(query_kwargs))
        elif any(tag_args):
            tags = tag_args[0]
            for tag in tag_args[1:]:
                tags = '{},{}'.format(tags, tag)
            path = '{}?tags={}'.format(path, tags)

        return json.loads(self.conn.get(path).text)

    def delete_tag(self, pk, data_id, tag_name):
        return json.loads(
            self.conn.delete('{}/{}/{}/labels/{}'.format(
                self.data_ep, pk, data_id, tag_name)).text)

    def get_enketo_editlink(self, pk, dataid, return_url):
        return json.loads(self.conn.get(
            '{}/{}/{}/enketo?return_url={}'.format(
                self.data_ep, pk, dataid, return_url)).text)
