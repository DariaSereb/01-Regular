import request_handler
import ssl
import os
import json
from sys import argv
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from socket import timeout

def make_forward_handler(upstream_url):

    class ForwardHTTPRequestHandler(BaseHTTPRequestHandler):

        def __init__(self, *args, **kwargs):
            super(ForwardHTTPRequestHandler, self).__init__(*args, **kwargs)

        def do_GET(self):

            json_string = {}

            reques = Request(upstream_url + self.path)

            for key in self.headers:
                reques.add_header(key, self.headers[key])

            try:
                r = urlopen(reques, timeout=1)
            except HTTPError as http_error:
                json_string['code'] = http_error.code
                json_string['headers'] = dict(http_error.headers)
            except URLError as url_error:
                print(url_error)
                raise
            except timeout:
                json_string['code'] = 'timeout'
            else:
                json_string['code'] = r.getcode()
                json_string['headers'] = dict(r.getheaders())
                res_data = r.read()

                try:
                    res_data_json = json.loads(res_data)
                except:
                    json_string['content'] = str(res_data)
                else:
                    json_string['json'] = res_data_json

            res_content = bytes(json.dumps(json_string,
                                           indent=4,
                                           sort_keys=False,
                                           ensure_ascii=False), 'utf-8')

            self.send_response(200, 'OK')
            self.send_header('Connection', 'close')
            self.send_header('Content-Type', 'text/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(res_content)

        def do_POST(self):

            req_content_legth = int(self.headers['Content-Length'])
            req_body = self.rfile.read(req_content_legth)
            json_string = {}

            try:
                reques = json.loads(req_body)
            except:
                json_string['code'] = 'invalid json'
            else:
                if (reques['url'] is None or
                    (reques['type'] == 'POST' and
                     reques['content'] is None)):
                    json_string['code'] = 'invalid json'
                else:
                    if reques['type'] == 'POST':

                        headers = reques['headers']
                        headers['Accept-Encoding'] = 'identity'                        

                        data = urlencode(reques['content']).encode('utf-8')

                        request = Request(reques['url'],data=data,headers=headers)
                    else:
                        request = Request(reques['url'],headers=reques['headers'])

                    req_timeout = int(reques['timeout']) if reques['timeout'] else 1

                    try:
                        r = urlopen(request, timeout=req_timeout)
                    except HTTPError as http_error:
                        json_string['code'] = http_error.code
                        json_string['headers'] = dict(http_error.headers)
                    except URLError as url_error:
                        print(url_error)
                        raise
                    except timeout:
                        json_string['code'] = 'timeout'
                    else:
                        json_string['code'] = r.getcode()
                        json_string['headers'] = dict(r.getheaders())
                        res_data = r.read()

                        try:
                            res_data_json = json.loads(res_data)
                        except:
                            json_string['content'] = str(res_data)
                        else:
                            json_string['json'] = res_data_json

            res_content = bytes(json.dumps(json_string,indent=4,sort_keys=False,ensure_ascii=False), 'utf-8')
            self.send_response(200, 'OK')
            self.send_header('Connection', 'close')
            self.send_header('Content-Type', 'text/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(res_content)

    return ForwardHTTPRequestHandler

if __name__ == '__main__':
    port = int(argv[1])
    upstream = argv[2]

    if not upstream.startswith('http://'):
        upstream = 'http://' + upstream

    Handler = make_forward_handler(upstream)

    httpd = HTTPServer(('', port), Handler)
    httpd.serve_forever()
