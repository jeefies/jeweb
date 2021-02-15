from .http_status import HTTP_STATUS_CODES

class Error:
    def __init__(self, exception, status = 404):
        self.exception = exception
        self.status_code = status

    @property
    def status(self):
        return HTTP_STATUS_CODES[self.status_code]
