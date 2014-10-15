class MockResponse(object):

    def __init__(self, status_code, reason=None, text=None):
        self.status_code = status_code
        self.reason = reason
        self.text = text
