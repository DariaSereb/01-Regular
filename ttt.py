import urllib
import json
from sys import argv
from socketserver import ThreadingMixIn
from http.server import HTTPServer, BaseHTTPRequestHandler

game_s = {}
max_id = 0

class T_Handler(BaseHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        super(T_Handler, self).__init__(*args, **kwargs)

    def do_GET(self):

        global game_s
        global max_id

        parsed_url = urllib.parse.urlparse(self.path)
        r_params = urllib.parse.parse_qs(parsed_url.query)
        r_path = parsed_url.path.strip('/')
        json = {}

        if r_path == 'start':

            name = r_params['name'][0] if 'name' in r_params else ''
            game = Game(name)
            game_s[max_id] = game
            json['id'] = max_id
            max_id += 1

        else:

            if 'game' not in r_params:
                self.send_error(400, 'Bad Request')
            elif int(r_params['game'][0]) not in game_s:
                json['status'] = 'bad'
                json['message'] = 'Game with id {} does not exists'.format(r_params['game'][0])
            elif r_path == 'status':
                game_id = int(r_params['game'][0])
                game = game_s[game_id]
                if game.status is None:
                    json['board'] = game.board
                    json['next'] = game.next
                else:
                    json['winner'] = game.status

            elif r_path == 'play':
                game_id = int(r_params['game'][0])
                player = int(r_params['player'][0])
                x = int(r_params['x'][0])
                y = int(r_params['y'][0])
                game = game_s[game_id]
                status, message = game.play(player, x, y)
                json['status'] = status
                json['message'] = message
        res_content = bytes(json.dumps(json,
                                       indent=4,
                                       sort_keys=False,
                                       ensure_ascii=False), 'utf-8')
        self.send_response(200, 'OK')
        self.send_header('Connection', 'close')
        self.send_header('Content-Type', 'text/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(res_content)


class Game():

    def __init__(self, name):
        self.board = [[0,0,0],[0,0,0],[0,0,0]]
        self.next = 1
        self.name = name
        self.status = None

    def _check_draw(self):
        for row in self.board:
            for cell in row:
                if cell == 0:
                    return False
        return True

    def play(self, player, x, y):
        if self.next == player:
            if self.board[x][y] == 0:
                self.board[x][y] = player
                self.next = 1 if player == 2 else 2
                if self._check_victory(x, y):
                    self.status = player
                elif self._check_draw():
                    self.status = 0
                return 'ok', 'ok'
            else:
                return 'bad', '{}, {} is already occupied'.format(x, y)
        else:
            return 'bad', 'It is player\'s {} turn'.format(self.next)

    def status(self):
        return self.status

    def _check_victory(self, x, y):
        if self.board[0][y] == self.board[1][y] == self.board[2][y]:
            return True
        if self.board[x][0] == self.board[x][1] == self.board[x][2]:
            return True
        if x == y and self.board[0][0] == self.board[1][1] == self.board[2][2]:
            return True
        if x + y == 2 and self.board[0][2] == self.board[1][1] == self.board[2][0]:
            return True
        return False



class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """ """

if __name__ == '__main__':
    port = int(argv[1])
    httpd = ThreadedHTTPServer(('', port), T_Handler)
    httpd.serve_forever()
