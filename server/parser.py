import os
import re
import mimetypes

from urllib.parse import unquote
from datetime import datetime

import server.status as status

HTTP_LINE = re.compile(r'^(?P<method>[A-Z]+)\s+' \
                        r'((?P<scheme>http[s]?)://)?' \
                        r'(?P<host>[\w*\.]*\w+)?/?' \
                        r'(?P<path>[^\?]*)?(\?[^.]*)?(\#.*)?\s+' \
                        r'(?P<http_ver>HTTP/1.[1|0])$')

VERSION = '1.1'

STATUS_PHRASE = {
    200 : 'OK',
    400 : 'BAD',
    403 : 'FORBIDDEN',
    404 : 'NOT FOUND',
    405 : 'METHOD NOT ALLOWED',
}

class Http():
    def __init__(self, request, root):
        self.Request = {}
        self.Response = {}

        self.Request['data'] = request
        self.Request['filename'] = root
        self.Request['headers'] = {}
        self.Request['method'] = None

        self.Response['status'] = None
        self.Response['headers'] = {}

    def parse(self, request):
        if request.find(status.BODY) > 0:
            request, _ = request.split(status.BODY)
        else:
            request = request

        if request.find(status.STRING) > 0:
            requestLine, headers = request.split(status.STRING, maxsplit=1)
            self._parse_headers(headers)
            self._parse_requestLine(requestLine)
        else:
            requestLine = request
            self._parse_requestLine(requestLine)

    def _parse_headers(self, headersRaw):
        if not headersRaw or type(headersRaw) != str:
            return False
        
        headersList = headersRaw.split(status.STRING)
        for header in headersList:
            key, value = list(map(lambda x: x.strip(), header.split(':', maxsplit=1)))
            self.Request['headers'][key] = value
        return True


    def _parse_requestLine(self, requestLine):
        if not requestLine or type(requestLine) != str:
            return False

        match = HTTP_LINE.search(requestLine)

        if not match:
            return False

        self.Request['method'] = match.group('method')
        self.Request['path'] = match.group('path')

        #если путь ведет в родительские каталоги
        if self.Request['path'].find('/..') > 0:
            self.Response['status'] = 404
            return False

        return True

    def get_response(self):
        if self.Response['status'] is None:
            if self.Request['method'] not in status.ALLOWED_METHODS:
                self.Response['status'] = 405
            else:
                filePath = os.path.join(self.Request['filename'], self.Request['path'])
                filePath = unquote(filePath)
                filePath = os.path.abspath(filePath)

                if not os.path.exists(filePath):
                    self.Response['status'] = 404
                else:
                    dirRequested = False

                    if os.path.isdir(filePath):
                        dirRequested = True
                        filePath = os.path.join(filePath, status.INDEX_FILE)
                        if not os.path.exists(filePath):
                            self.Response['status'] = 403

                    if os.path.isfile(filePath):
                        if self.Request['path'].endswith('/') and not dirRequested:
                            self.Response['status'] = 404
                        else:
                            self.Request['filename'] = filePath
                            self.Response['mimetype'], _ = mimetypes.guess_type(filePath)
                            self.Response['headers'] = {
                                'Content-Length': str(os.path.getsize(filePath)),
                                'Content-Type': self.Response['mimetype'],
                            }
                            self.Response['status'] = 200
        return self.to_string()


    def _default_headers(self):
        return {
            'Connection': 'close',
            'Date': datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT'),
            'Server': status.SERVER
        }

    def build_headers(self, headersDict):
        headersDict = {**headersDict, **self._default_headers()}
        return status.STRING.join(
            "{!s}: {!s}".format(key, val) for (key, val) in headersDict.items())


    def build_response_line(self, status):
        message = STATUS_PHRASE.get(status) or ''
        return 'HTTP/{} {} {}'.format(VERSION, status, message)


    def to_string(self):
        response_line = self.build_response_line(self.Response['status'])
        headers = self.build_headers(self.Response['headers'])
        return r'{}{}{}{}'.format(response_line, status.STRING, headers, status.BODY)