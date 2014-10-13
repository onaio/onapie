class ApiException(Exception):

    def __init__(self, msg, response=None):
        self.msg = msg
        if response is not None:
            self.api_response = response
            self.msg = u'Api Error: {}, {}'.format(
                self.api_response.status_code, self.api_response.reason)
        self.api_response = response
        Exception.__init__(self, msg)

    def __str__(self):
        return self.msg


class ClientException(ApiException):

    def __init__(self, msg, response=None, request=None):
        super(ClientException, self).__init__(msg, response)
