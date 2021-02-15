import codecs
from email.utils import formatdate
from types import GeneratorType
from collections import deque

from .http_status import (HTTP_STATUS_CODES, ERRORS)


SEP = b"\r\n"
SIZE = 1024 << 2

class Header:
    START = 'HTTP/1.0 '
    SERVER = 'Jeweb/0.0.1 Python/3'
    def __init__(self, cnf={}):
        self.status = 200
        self.date = formatdate(usegmt=1)
        self.content_type = 'text/html'
        self.server = 'python'
        self.charset = 'utf-8'
        self.lines = deque()

    def __setitem__(self, index, val):
        index = index.lower().replace('-', '_')
        setattr(self, index, val)

    def __getitem__(self, index):
        index = index.lower().replace('-', '_')
        return getattr(self, index)

    def __getattr__(self, index, e=None):
        return self.__dict__.get(index, e)

    def tolines(self):
        lines = self.lines
        lines.append(self.START +  HTTP_STATUS_CODES[self.status])

        if not self.content_type:
            self.content_type = 'text/html'


        lines.append("Content-Type: " + self.content_type + '; charset=' + self.charset)
        lines.append("Server: " + self.SERVER)
        lines.append("Date: " + self.date)

        return lines

    def write(self, key, val):
        self.lines.append("{}: {}".format(key, val))

    def tobyte(self):
        if not self.lines:
            self.tolines()
        return SEP.join(map(codecs.encode, self.lines))


class Response:
    START = b'HTTP/1.0 '
    def __init__(self, data, status = 200):
        if not isinstance(data, (str, bytes, bytearray, GeneratorType)):
            if isinstance(data, Response):
                data = data._data
            else:
                raise TypeError("A str, bytes, bytearray, generator or a Response object is required. Not Type %s" % type(r))

        if isinstance(data, str):
            data = data.encode('utf-8')
        self._data = data

        self.header = Header()
        self.header.status = status

    def tobyte(self):
        self.header.tolines()
        self.header.write("Content-Length", len(self.data))
        return self.header.tobyte()

    @property
    def status_code(self):
        return self.header.status

    @property
    def status(self):
        return HTTP_STATUS_CODES[self.status_code]

    @status_code.setter
    def status_code(self, val):
        self.header.status = int(val)

    @property
    def single(self):
        return not isinstance(self._data, GeneratorType)

    @property
    def data(self):
        return self._data
