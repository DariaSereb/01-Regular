import json
from sys import argv
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib import request


class Handler(BaseHTTPRequestHandler):

    def do_POST(self):
        length = int(self.headers.get('content-length'))
        try:
            data = json.loads(self.rfile.read(length))
            type = data['type'] if 'type' in data else 'GET'
            url = data['url']
            headers = data['headers'] if 'headers' in data else dict()
            headers['Accept-Encoding'] = 'identity'
            if 'content-type' not in (header.lower() for header in headers):
                headers['Content-Type'] = 'application/json; charset=utf-8'
            cont = data['content'] if type == 'POST' else None
            if cont:
                cont = json.dumps(cont).encode('utf-8')
            timeout = data['timeout'] if 'timeout' in data else 1

            req = request.Request(method=type, url=url, headers=headers, data=cont)

        except:
            return self.send({'code': 'invalid json'})

        try:
            with request.urlopen(req, timeout=timeout) as response:
                res_content = response.read()
                res_content = res_content.decode('utf-8')

            new_response = self.prepare_response(response.code, response.getheaders(), res_content)
            self.send(new_response)
        except:
            self.send({'code': 'timeout'})


    def do_GET(self):
        r_headers = self.headers
        r_headers['Accept-Encoding'] = 'identity'

        del r_headers['Host']
        upstr = argv[2]

        if not upstr.startswith('http://') and not upstr.startswith('https://'):
            upstr = 'http://' + upstr
        req = request.Request(method='GET', url=upstr, headers=r_headers)

        with request.urlopen(req, timeout=1) as response:
            res_content = response.read()
            res_content = res_content.decode('utf-8')
            try:
                new_response = self.prepare_response(200, response.getheaders(), res_content)
                self.send(new_response)
            except:
                self.send({'code': 'timeout'})



    def prepare_response(self, status_code, headers, cont):
        response = {'code': status_code}

        if headers:
            response['headers'] = {}
            for header in headers:
                response['headers'][header[0]] = header[1]

        if cont:
            try:
                response['json'] = json.loads(cont)
            except:
                response['content'] = cont

        return response

    def send(self, response):
        cont = json.dumps(response, indent=4)
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(cont)))
        self.end_headers()
        self.wfile.write(bytes(cont, 'UTF-8'))


port = int(argv[1])
server = HTTPServer(('', port), Handler)
server.serve_forever()

