#!/usr/bin/python3

import sys
import asyncio
from aiohttp import web


class game_run:

    def __init__(self):
        self.games = {}

    def new_game(self, name):
        id_game= len(self.games.keys())
        if id_game not in self.games.keys():
            self.games[id_game] = (str(name), GameBoard())
            return id_game
        else:
            return None

    def get_list(self):
        out_put = []
        for key, value in self.games.items():
            if value[1].waiting_for_player:
                dict = {}
                dict['id'] = int(key)
                dict['name'] = value[0]
                out_put.append(dict)
        return out_put

    def get_game_by_id(self, id_game):
        try:
            return self.games[id_game][1]
        except Exception:
            return None

class GameBoard:

    def __init__(self):
        self.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.next = 1
        self.locked = False
        self.winner = None
        self.waiting_for_player = True

    def lock_n_move(self, player, x, y):
        if not self.locked:
            self.locked = True
            result = self.make_move(player, x, y)
            self.locked = False
            return result
        else:
            return False

    def make_move(self, player, x, y):
            if int(player) != self.next:
                return False, "Next player should be " + str(self.next)
            elif self.winner is not None:
                return False, "Game is over"
            else:
                if int(x) > len(self.board[0]) - 1 or int(y) > len(self.board) - 1:
                    return False, "Out of range"
                else:
                    if self.board[int(x)][int(y)] == 0:
                        self.board[int(x)][int(y)] = int(player)
                        if int(player) == 2:
                            self.waiting_for_player = False
                        if self.player_win_check(player):
                            self.winner = int(player)
                        elif not self.another_move_is_possible():
                            self.winner = 0
                        self.next = (int(player) %2) + 1
                        return True, None
                    else:
                        return False, "Field is already taken"

    def player_win_check(self, player):
        player = int(player)
        for i in range(0, 3):
            for j in range(0, 3):
                if self.board[i][j] == player:
                    if (self.board[i][0] == player and self.board[i][1] == player and self.board[i][2] == player) or (self.board[0][j] == player and self.board[1][j] == player and self.board[2][j] == player):
                        return True
        if(self.board[0][0] == player and self.board[1][1] == player and self.board[2][2] == player) or (self.board[0][2] == player and self.board[1][1] == player and self.board[2][0] == player):
            return True
        return False

    def another_move_is_possible(self):
        i = 0
        j = 0
        for i in range(0, 3):
            for j in range(0, 3):
                if self.board[i][j] == 0:
                    return True
        return False

    def get_winner(self):
        return self.winner

    def get_status(self):
        if self.winner is None:
            return self.board, self.next
        else:
            return self.board, self.winner


allGames = game_run()


@asyncio.coroutine
async def handle_start(request):
    try:
        name = request.query['name']
    except Exception:
        name = ''
    js = {}
    js['id'] = int(allGames.new_game(name))
    return web.json_response(status=200, data=js)


@asyncio.coroutine
async def handle_status(request):
    try:
        id_game = request.query['game']
    except Exception:
        err = {}
        err['error'] = 'request does not contain game parameter'
        return web.json_response(status=404, data=err)
    try:
        int(id_game)
    except Exception:
        err = {}
        err['error'] = 'cannot parse game id'
        return web.json_response(status=400, data=err)

    js = {}
    game = allGames.get_game_by_id(int(id_game))

    if game is None:
        err = {}
        err['error'] = 'No game with id ' + str(id_game)
        return web.json_response(status=400, data=err)
    if game.get_winner() is None:
        js['board'], js['next'] = game.get_status()
    else:
        js['board'], js['winner'] = game.get_status()
    return web.json_response(status=200, data=js)


@asyncio.coroutine
async def handle_play(request):
    try:
        id_game = request.query['game']
        player = request.query['player']
        x = request.query['x']
        y = request.query['y']
    except Exception:
        err = {}
        err['error'] = 'request does not contain game, player or coordinates parameters'
        return web.json_response(status=400, data=err)
    try:
        int(id_game)
        int(player)
        int(x)
        int(y)
    except Exception:
        err = {}
        err['error'] = 'cannot parse game id, player or coordinates integers'
        return web.json_response(status=400, data=err)

    game = allGames.get_game_by_id(int(id_game))

    if game is None:
        err = {}
        err['error'] = 'No game with id ' + str(id_game)
        return web.json_response(status=400, data=err)
    js = {}
    success, message = game.make_move(player, int(x), int(y))
    if success:
        js['status'] = "ok"
    else:
        js['status'] = 'bad'
        js['message'] = message
    return web.json_response(status=200, data=js)


@asyncio.coroutine
async def handle_list(request):
    list = allGames.get_list()
    return web.json_response(status=200, data=list)


def aio_server(port):
    application = web.Application()
    application.router.add_route('GET', '/start{tail:.*}', handle_start)
    application.router.add_route('GET', '/status{tail:.*}', handle_status)
    application.router.add_route('GET', '/play{tail:.*}', handle_play)
    application.router.add_route('GET', '/list{tail:.*}', handle_list)
    web.run_app(application, host='localhost', port=port)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        aio_server(int(sys.argv[1]))
    else:
        print("Wrong number of arguments")
