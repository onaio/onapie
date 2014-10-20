from onapie.exceptions import ClientException
import json


class XlsFormsManager(object):

    def __init__(self, conn, api_entrypoint, exports_entrypoint=None):
        self.conn = conn
        self.forms_ep = api_entrypoint
        self.exports_ep = 'exports'

    def create(self, xls_path=None, xls_url=None, owner=None):
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

        return json.loads(self.conn.post(self.forms_ep,
                                         xls_path, xls_url).text)

    def list(self, owner=None):
        """Returns a list of forms

        .. attribute:: owner

            Optional. Get forms by owner username
        """
        query = self.forms_ep

        if owner is not None:
            query = '{}?owner={}'.format(query, owner)

        return json.loads(
            self.conn.get(query).text)

    def get(self, pk, representation=None, *tag_args):
        """Get Form Information or representation"""
        path = '{}/{}'.format(self.forms_ep, pk)

        if representation is not None:
            if representation not in ['json', 'xml', 'xls', 'csv']:
                raise ClientException(
                    'Invalid representation:- {}. Options are '
                    'json, csv, xml or xls'.format(representation))
            path = '{}/form.{}'.format(path, representation)

        if any(tag_args):
            tags = tag_args[0]
            for tag in tag_args[1:]:
                tags = '{},{}'.format(tags, tag)

            path = '{}?tags={}'.format(path, tags)

        if representation and representation != 'json':
            return self.conn.get(path).text
        else:
            return json.loads(self.conn.get(path).text)

    def export(self, pk, data_format=None):
        path = '{}/{}'.format(self.forms_ep, pk)
        if data_format is not None:
            if data_format not in ['json', 'xml', 'xls', 'csv']:
                raise ClientException(
                    'Invalid representation:- {}. Options are '
                    'json, csv, xml or xls'.format(data_format))
            path = '{}.{}'.format(path, data_format)

        if data_format and data_format != 'json':
            return self.conn.get(path).text

    def update(self, pk, uuid, description, owner, public, public_data):
        """Update Form"""

        form = ('uuid={}&description={}&owner={}'
                '&public={}&public_data={}').format(uuid, description, owner,
                                                    public, public_data)

        return json.loads(self.conn.put('{}/{}'.format(self.forms_ep, pk),
                          None, form).text)

    def patch(self, pk, **kwargs):
        """Update Form Properties"""

        args = '{}={}'.format(*kwargs.items()[0])
        for key, value in kwargs.items()[1:]:
            args = '{}&{}={}'.format(args, key, value)

        return json.loads(
            self.conn.patch('{}/{}'.format(self.forms_ep, pk),
                            None, args).text)

    def delete(self, pk):
        """Deletes your form"""

        resp = self.conn.delete('{}/{}'.format(self.forms_ep, pk))
        if resp.status_code != 204:
            raise ClientException(
                'Invalid api delete response: {}, {}'.format(
                    resp.status_code, resp.reason))

    # Tags
    def get_tags(self, pk):
        """Get list of Tags for a specific Form"""

        return json.loads(
            self.conn.get('{}/{}/labels'.format(self.forms_ep, pk)).text)

    def set_tag(self, pk, *tag_args):
        """Tag forms"""

        tags = json.dumps({'tags': tag_args})

        return json.loads(
            self.conn.post('{}/{}/labels'.format(self.forms_ep, pk),
                           tags).text)

    def remove_tag(self, pk, tag):
        """Removes a tag"""

        return json.loads(
            self.conn.delete('{}/{}/labels/{}'.format(self.forms_ep,
                                                      pk, tag)).text)

    def get_webformlink(self, pk):
        return json.loads(
            self.conn.get('{}/{}/enketo'.format(self.forms_ep, pk)).text)

    def get_formdata(self, pk, export_format):
        # TODO: Implement when API behaves
        raise ClientException('This has not Implemented.')

    def share(self, pk, username, role):
        """Share a form with a specific user"""

        payload = {'username': username}

        if role in ['readonly', 'dataentry', 'editor', 'manager']:
            payload['role'] = role

        return json.loads(
            self.conn.post('{}/{}/share'.format(self.forms_ep, pk),
                           payload).text)

    def clone_to_user(self, pk, username):
        """Clone a form to a specific user account"""

        return json.loads(
            self.conn.post('{}/{}/clone'.format(self.forms_ep, pk),
                           'username={}'.format(username)).text)
