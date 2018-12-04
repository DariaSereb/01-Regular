import os
import json
import socket
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode

def handler(upstream_url):
    class ForwardHTTPRequestHandler(BaseHTTPRequestHandler):

        def __init__(self, *args, **kwargs):
            super(ForwardHTTPRequestHandler, self).__init__(*args, **kwargs)



        def send_request(self, url, headers, data=None, timeout=1):
            json = {}
            request_1 = Request(url, headers=headers, data=data)
            try:
                result = urlopen(request_1, timeout=timeout)
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
                data1 = result.read()
                try:
                    result_data_json = json.loads(data1)
                except:
                    json['content'] = str(data1)
                else:
                    json['json'] = result_data_json
            return json




        def do_GET(self):
            url = upstream_url + self.path
            headers = {}
            for key in self.headers:
                headers[key] = self.headers[key]

            json = self.send_request(url, headers)
            result_content = bytes(json.dumps(json,indent=4,sort_keys=False,ensure_ascii=False), 'utf-8')
            self.send_response(200, 'OK')
            self.send_header('Connection', 'close')
            self.send_header('Content-Type', 'text/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(result_content)





        def do_POST(self):
            request_legth = int(self.headers['Content-Length'])
            request_b = self.rfile.read(request_legth).decode('utf-8')
            json = {}
            try:
                request_1 = json.loads(request_b)
            except:
                json['code'] = 'invalid json'
            else:
                if (request_1['url'] is None or
                    (request_1['type'] == 'POST' and
                     request_1['content'] is None)):
                    json['code'] = 'invalid json'
                else:
                    if request_1['type'] == 'POST':
                        headers = request_1['headers']
                        headers['Accept-Encoding'] = 'identity'
                        data = urlencode(request_1['content']).encode('utf-8')
                    else:
                        headers = request_1['headers']

                    req_timeout = int(request_1['timeout']) if request_1['timeout'] else 1
                    json = self.send_request(request_1['url'], headers, data, req_timeout)
            result_content = bytes(json.dumps(json,indent=4,sort_keys=False,ensure_ascii=False), 'utf-8')

            self.send_response(200, 'OK')
            self.send_header('Connection', 'close')
            self.send_header('Content-Type', 'text/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(result_content)


    return ForwardHTTPRequestHandler
