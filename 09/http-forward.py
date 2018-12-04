import os
import json
import socket
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlencode
from sys import argv
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

def handler(upstream_url):
    class ForwardHTTPRequestHandler(BaseHTTPRequestHandler):

        def __init__(self, *args, **kwargs):
            super(ForwardHTTPRequestHandler, self).__init__(*args, **kwargs)


        def send_request(self, url, headers, data=None, timeout=1):

            json = {}
            request= Request(url, headers=headers, data=data)

            try:
                result = urlopen(request, timeout=timeout)

            except HTTPError as http_error:

                json['code'] = http_error.code
                json['headers'] = dict(http_error.headers)
            except URLError as url_error:
                print(url_error)
                raise
            except socket.timeout:
                json['code'] = 'timeout'
            else:
                json['code'] = result.getcode()
                json['headers'] = dict(result.getheaders())

                result_data = result.read()

                try:
                    result_data_json = json.loads(result_data)
                except:
                    json['content'] = str(result_data)
                else:
                    json['json'] = result_data_json

            return json

        def do_POST(self):

            request_legth = int(self.headers['Content-Length'])
            request_body = self.rfile.read(request_legth).decode('utf-8')
            json = {}

            try:
                request= json.loads(request_body)
            except:
                json['code'] = 'invalid json'
            else:
                if (request['url'] is None or
                    (request['type'] == 'POST' and
                     request['content'] is None)):
                    json['code'] = 'invalid json'
                else:
                    if request['type'] == 'POST':

                        headers = request['headers']
                        headers['Accept-Encoding'] = 'identity'

                        data = urlencode(request['content']).encode('utf-8')

                    else:

                        headers = request['headers']

                    request_timeout = int(request['timeout']) if request['timeout'] else 1

                    json = self.send_request(request['url'], headers, data, request_timeout)

            result_content = bytes(json.dumps(json,
                                           indent=4,
                                           sort_keys=False,
                                           ensure_ascii=False), 'utf-8')

            self.send_response(200, 'OK')
            self.send_header('Connection', 'close')
            self.send_header('Content-Type', 'text/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(result_content)

        def do_GET(self):

            url = upstream_url + self.path
            headers = {}
            for key in self.headers:
                headers[key] = self.headers[key]

            json = self.send_request(url, headers)

            result_content = bytes(json.dumps(json,
                                           indent=4,
                                           sort_keys=False,
                                           ensure_ascii=False), 'utf-8')

            self.send_response(200, 'OK')
            self.send_header('Connection', 'close')
            self.send_header('Content-Type', 'text/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(result_content)


    return ForwardHTTPRequestHandler



if __name__ == '__main__':
    port = int(argv[1])
    upstream = argv[2]

    if (not upstream.startswith('http://')
        and not upstream.startswith('https://')):
        upstream = 'http://' + upstream


    Handler = handler(upstream)

    httpd = HTTPServer(('', port), Handler)
    httpd.serve_forever()
