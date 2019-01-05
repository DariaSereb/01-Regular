import json
import urllib
from sys import argv
from game import Game
from socketserver import ThreadingMixIn
from http.server import HTTPServer, BaseHTTPRequestHandler

games = {}
max_id = 0

class TicTacToeHandler(BaseHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        super(TicTacToeHandler, self).__init__(*args, **kwargs)

    def do_GET(self):

        global games
        global max_id

        parsed_url = urllib.parse.urlparse(self.path)
        r_params = urllib.parse.parse_qs(parsed_url.query)
        r_path = parsed_url.path.strip('/')
        r_json = {}

        if r_path == 'start':

            name = r_params['name'][0] if 'name' in r_params else ''

            game = Game(name)
            games[max_id] = game
            r_json['status'] = 'ok'
            r_json['message'] = 'ok'
            r_json['id'] = max_id
            max_id += 1

        else:

            if r_path == 'list':
                game_list = []

                for game_id in games:
                    game = games[game_id]

                    if not game.full:
                        game_list.append({
                            'id': game_id,
                            'name': game.name
                        });

                r_json['games'] = game_list

            elif 'game' not in r_params:

                self.send_error(400, 'Bad Request')

            elif int(r_params['game'][0]) not in games:

                r_json['status'] = 'bad'
                r_json['message'] = 'Game with id {} does not exists'.format(r_params['game'][0])

            elif r_path == 'status':

                game_id = int(r_params['game'][0])
                game = games[game_id]

                if game.status is None:
                    r_json['board'] = game.board
                    r_json['full'] = game.full
                    r_json['next'] = game.next
                else:
                    r_json['board'] = game.board
                    r_json['winner'] = game.status

            elif r_path == 'play':

                game_id = int(r_params['game'][0])
                player = int(r_params['player'][0])
                x = int(r_params['x'][0])
                y = int(r_params['y'][0])

                game = games[game_id]
                status, message = game.play(player, x, y)

                r_json['status'] = status
                r_json['message'] = message
                r_json['board'] = game.board

            elif r_path == 'join':

                game_id = int(r_params['game'][0])

                if games[game_id].full:
                    r_json['status'] = 'bad'
                    r_json['message'] = 'Game with id {} is already full'.format(game_id)

                else:
                    games[game_id].full = True
                    r_json = {
                        'status': 'ok',
                        'message': 'ok',
                        'id': game_id
                    }

            else:
                self.send_error(404, 'Not Found')

        r_content = bytes(json.dumps(r_json,
                                       indent=4,
                                       sort_keys=False,
                                       ensure_ascii=False), 'utf-8')

        self.send_response(200, 'OK')
        self.send_header('Connection', 'close')
        self.send_header('Content-Type', 'text/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(r_content)


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """handle requests """

if __name__ == '__main__':
    port = int(argv[1])
    httpd = ThreadedHTTPServer(('', port), TicTacToeHandler)
    httpd.serve_forever()
