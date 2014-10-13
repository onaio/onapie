from onapie.exceptions import ClientException
import json


class XlsFormsManager(object):

    def __init__(self, conn, api_entrypoint):
        self.conn = conn
        self.api_ep = api_entrypoint or '/api/v1'
        self.forms_path = '{}/{}'.format(self.api_ep, 'forms')
        self.exports_path = '{}/{}'.format(self.api_ep, 'exports')

    def upload(self, xls_path=None, xls_url=None, owner=None):
        """Uploads an XLSForm

        .. attribute::xls_path

            Full path to the xlsform file. Mutually exclusive with xls_url

        .. attribute::xls_url

            A url to an xlsform. Mutually exclusive with xls_path

        .. attribute::owner

            Optional. username to the target account (Optional)
            TODO(kazikubwa@gmail.com): pass owner to the REST api?
        """
        if (xls_path is None) == (xls_url is None):
            raise ClientException(u'You must provide a path or a url '
                                  'for creation. The two args are '
                                  'mutually exclusive!')

        return json.loads(self.conn.post('{}'.format(
            self.forms_path), xls_path, xls_url).text)

    def list(self, owner=None):
        """Returns a list of forms

        .. attribute:: owner

            Optional. Get forms by owner username
        """
        query = '{}'.format(self.forms_path)

        if owner is not None:
            query = '{}?owner={}'.format(query, owner)

        return json.loads(
            self.conn.get(query).text)

    def get(self, pk, represetation=None, **tag_args):
        """Get Form Information or representation"""
        path = '{}/{}'.format(self.forms_path, pk)

        if represetation in ['json', 'xml', 'xls']:
            path = '{}/form.{}'.format(path, represetation)

        tags = 'tags='
        for tag in tag_args:
            tags = '{},'.format(tags, tag)

        path = '{}?{}'.format(path, tags)

        return json.loads(self.conn.get(path).text)

    def update(self, pk, uuid, description, owner, public, public_data):
        """Update Form"""

        form = \
            'uuid={}&description={}&owner={}&public={}&public_data={}'.format(
                uuid, description, owner, public, public_data)

        return json.loads(self.conn.put('{}/{}'.format(self.forms_path, pk),
                          None, form).text)

    def patch(self, pk, **kwargs):
        """Update Form Properties"""

        args = ''
        for key, value in kwargs.items():
            args = '{}&{}={}'.format(args, key, value)

        return json.loads(
            self.conn.patch('{}/{}'.format(self.forms_path, pk),
                            None, args).text)

    def delete(self, pk):
        """Deletes your form"""

        resp = self.conn.delete('{}/{}'.format(self.forms_path, pk))
        if resp.status_code != 204:
            raise ClientException(
                'Invalid api delete response: {}, {}'.format(
                    resp.status_code, resp.reason))

    # Tags
    def get_tags(self, pk):
        """Get list of Tags for a specific Form"""

        return json.loads(
            self.conn.get('{}/{}/labels'.format(self.forms_path, pk)).text)

    def set_tag(self, pk, *tag_args):
        """Tag forms"""

        tags = json.puts({'tags': tag_args})

        return json.loads(
            self.conn.post('{}/{}/labels'.format(self.forms_path, pk),
                           tags).text)

    def remove_tag(self, pk, tag):
        """Removes a tag"""

        return json.loads(
            self.conn.delete('{}/{}/labels/{}'.format(self.forms_path,
                                                      pk, tag)).text)

    def get_webformlink(self, pk):
        return json.loads(
            self.conn.get('{}/{}/enketo'.format(self.forms_path, pk)).text)

    def get_formdata(self, pk, export_format):
        return self.conn.get('{}/{}.{}'.format(self.exports_path,
                                               pk, export_format),
                             stream=True).raw

    def share(self, pk, username, role):
        """Share a form with a specific user"""

        payload = {'username': username}

        if role in ['readonly', 'dataentry', 'editor', 'manager']:
            payload['role'] = role

        resp = self.conn.post('{}/{}/share'.format(self.forms_path, pk),
                              payload)
        if resp.status_code != 204:
            raise ClientException(
                'Invalid api form share response: {}, {}'.format(
                    resp.status_code, resp.reason))

    def clone_to_user(self, pk, username):
        """Clone a form to a specific user account"""

        return json.loads(
            self.conn.post('{}/{}/clone'.format(self.forms_path, pk),
                           'username={}'.format(username)).text)