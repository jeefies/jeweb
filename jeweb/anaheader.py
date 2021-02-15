import io
import urllib.parse as urlpar
from .http_status import MULTI_HEADINGS


SEP = b'\r\n'
SEP2 = b'\r\n\r\n'
SIZE = 1024 << 2


class AnaHeader:
    def __init__(self, header, conn):
        self.args = dict()
        self.values = dict()
        self.di = self.analyze(header)
        self.orgin = header
        self.conn = conn

    def readFully(self):
        if not self.method == "POST":
            return

        cl = self.di['Content_Length']
        conn = self.conn
        file = io.BytesIO()
        for i in range(0, cl, SIZE):
            file.write(conn.read(SIZE))
        while file.tell() != cl:
            file.write(conn.read(SIZE))

        self.file = file

    def analyze(self, header):
        def d(x):
            return x.decode('ascii')

        r = dict()
        if not header.endswith(SEP2) and SEP2 in header:
            header, kvs = header.split(SEP2)
            self.values = self.analyze_kv(kvs)

        li = header.split(SEP)

        l1 = li.pop(0)
        r['method'], r['url'], _ = self.method, self.url, _ = d(l1).split(' ')
        self.path, args, self.fragment = self.analyze_url(self.url)
        self.args.update(args)

        for l in li:
            if l == b'':
                continue
            prefix, content = l.split(b': ', 1)
            if prefix not in MULTI_HEADINGS:
                content = (content.split(b';') if b';' in content 
                        else content.split(b',') if b',' in content
                        else [content])

            r[prefix] = content

        return r

    @staticmethod
    def analyze_kv(kvs):
        kvs = kvs.split(b'&') if b'&' in kvs else [kvs]
        return dict(tuple(kv.split(b'=') for kv in kvs))

    @staticmethod
    def analyze_url(url):
        par = urlpar.urlparse(url)
        path = par.path
        if not path == b'/':
            path = path.rstrip('/')
        querys = par.query

        r = dict()
        if querys:
            q = querys.split('&') if '&' in querys else [querys]
            uq = urlpar.unquote
            for kv in q:
                k, v = kv.split()
                r[uq(k)] = uq(v)

        return path, r, par.fragment
