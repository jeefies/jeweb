import sys
import socket
import urllib.parse as urlpar
from threading import Thread

from .error import Error
from .anaheader import AnaHeader
from .response import Response


SEP2 = b"\r\n\r\n"

class Jeweb:
    MAX_THREADS = 5
    MAX_CONNECTION = 100

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.urls = dict()
        self.errors = dict()

    def addHandler(self, url, handler):
        path = urlpar.urlparse(url).path
        if not path == '/':
            path = path.rstrip('/')
        self.urls[path] = handler

    def handler(self, url):
        def wrapper(func):
            self.addHandler(url, handler)
            return func
        return wrapper

    def handle(self, conn, addr):
        header = AnaHeader(conn.recv(1024), conn)

        handler = self.urls.get(header.url, None)
        if not handler:
            print(f"404 Not Found for {header.url}")
            eh404 = self.errors.get(404)
            if not eh404:
                r = Response(ERRORS[404], 404)
            else:
                e = Error(None, 404)
                r = eh404(header, addr, e)
        else:
            print(f"Accept request {header.url} from %s:%s" % addr)
            try:
                try:
                    r = getattr(handler, header.method.upper())(header, addr)
                except TypeError:
                    r = getattr(handler, header.method.upper())(handler, header, addr)
            except Exception as _e:
                eh500 = self.errors.get(500)
                e = Error(_e, 500)
                eh500(header, addr, e)

        if not isinstance(r, Response):
            r = Response(r)
        
        b = r.tobyte()
        conn.send(b + SEP2)
        if r.single:
            conn.send(r.data)
        else:
            for d in r.data:
                conn.send(r.data)
        conn.close()

    def run(self, host = '0.0.0.0', port = 8000):
        addr = (host, port)
        self.sock.bind(addr)
        self.sock.listen(self.MAX_CONNECTION)
        print(self.urls)

        print(addr)
        print('Start Server at ', host, ':', port, sep='')
        """
        try:
            self._thr()
        except KeyboardInterrupt:
            print('\rInterrupt...')
            sys.exit(0)
        
        """
        thrs = [Thread(None, self._thr, 'jeweb%d' % d) for d in range(self.MAX_THREADS)]
        for t in thrs:
            t.setDaemon(True)
        for t in thrs:
            t.start()
        try:
            while 1:
                pass
        except KeyboardInterrupt:
            print('\rInterrupt...')
            sys.exit(0)
        #"""
    
    def _thr(self):
        while True:
            args = self.sock.accept()
            self.handle(*args)

    def addErrorHandler(self, status, func):
        self.errors[status] = func
        
    def errorHandler(self, status):
        def wrapper(func):
            self.addErrorHandler(status, func)
            return func
        return wrapper
