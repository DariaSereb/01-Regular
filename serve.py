from sys import argv
import urllib
import os
from socketserver import ThreadingMixIn
from http.server import HTTPServer
from http.server import CGIHTTPRequestHandler

def handler(port, dir):

    class Handler(CGIHTTPRequestHandler):

        cgi_dirc = [os.path.normpath(os.path.join(os.getcwd(), dir))]

        def get_path(self, path):

            return os.path.normpath(os.path.join(os.getcwd(), dir, path))

        def run(self, path, params):

            print('run cgi script')
            print(path)

            self.cgi_info = os.path.relpath(dir), path + '?' + params
            self.run_cgi()

        def send_file(self, file_path):

            with open(file_path, 'rb') as f:

                size = os.path.getsize(file_path)
                data = f.read()

                self.send_response(200)
                self.send_header('Content-Length', str(size))
                self.end_headers()
                self.wfile.write(data)


        def do_POST(self):
            request_content = int(self.headers['Content-Length'])
            request_body = self.rfile.read(request_content).decode('utf-8')

            p_url = urllib.parse.urlparse(self.path)
            request_par = p_url.query
            request_path = self.get_path(p_url.path[1:])

            if os.path.isfile(request_path):
                if request_path.endswith('.cgi'):
                    self.run(p_url.path[1:], request_par)
                else:
                    self.send_file(request_path)
            else:
                self.send_error(403, 'Error')

        def do_GET(self):

            p_url = urllib.parse.urlparse(self.path)
            request_par = p_url.query
            request_path = self.get_path(p_url.path[1:])

            print(request_path)

            if os.path.isfile(request_path):
                if request_path.endswith('.cgi'):
                    self.run(p_url.path[1:], request_par)
                else:
                    self.send_file(request_path)
            else:
                self.send_error(403, 'Error')



    return Handler

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """ """

if __name__ == '__main__':
    port = int(argv[1])
    dir = argv[2]

    Handler = handler(port, dir)

    httpd = ThreadedHTTPServer(('', port), Handler)
    httpd.serve_forever()
