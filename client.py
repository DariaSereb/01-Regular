#!/usr/bin/python3

import sys
import asyncio
import aiohttp



class GameInfo:
    def __init__(self):
        self.port = 9001
        self.host = 'localhost'   
        self.selected_game_id = None
        self.selected_player = None
        self.next_player = None
        self.winner = None
        self.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.player_waiting = False

    def reset_game(self):
        self.winner = None
        self.next_player = None
        self.player_waiting = False
        self.selected_game_id = None
        self.selected_player = None


game_inf = GameInfo()


def run_f(task, *, loop=None):
    if loop is None:
        if sys.platform.startswith('win'):
            loop = asyncio.ProactorEventLoop()
            asyncio.set_event_loop(loop)
        else:
            loop = asyncio.get_event_loop()
    return loop.run_until_complete(asyncio.ensure_future(task, loop=loop))


def sync_wait(task, loop=None):
    if loop is None:
        if sys.platform.startswith('win'):
            loop = asyncio.ProactorEventLoop()
            asyncio.set_event_loop(loop)
        else:
            loop = asyncio.get_event_loop()
    return loop.run_until_complete(task)


@asyncio.coroutine
async def draw_board():
    global game_inf
    await get_status()
    if game_inf.next_player != game_inf.selected_player:
        if not game_inf.player_waiting:
            print('waiting for other player')
            game_inf.player_waiting = True
    else:
        game_inf.player_waiting = False
    if len(game_inf.board) > 0:
        for i in range(0, len(game_inf.board)):
            for j in range(0, len(game_inf.board[0])):
                if game_inf.board[i][j] == 1:
                    print('X', end='')
                elif game_inf.board[i][j] == 2:
                    print('O', end='')
                else:
                    print('_', end='')
            print(end='\n')
        await asyncio.sleep(1)


async def get_status():
    global game_inf
    result = await call_status()
    if result is not None:
        try:
            game_inf.board = result['board']
        except Exception:
            pass
        try:
            game_inf.next_player = result['next']
        except Exception:
            pass
        try:
            game_inf.winner = result['winner']
        except Exception:
            pass


async def call_status():
    global game_inf
    url = 'http://' + game_inf.host + ':' + str(game_inf.port) + '/status?game=' + str(game_inf.selected_game_id)
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url=url) as resp:
                try:
                    result = await resp.json()
                    return result
                except Exception as e:
                    return None
        except Exception as e:
            return None


@asyncio.coroutine
async def join_to_game(input_id):
    global game_inf
    url = 'http://' + game_inf.host + ':' + str(game_inf.port) + '/status?game=' + str(input_id)
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url=url) as resp:
                if resp.status == 200:
                    game_inf.selected_game_id = input_id
                    game_inf.selected_player = 2
                try:
                    json = await resp.json()
                    error = json['error']
                    return error
                except Exception:
                    pass
                return None
        except Exception as e:
            game_inf.selected_player = None
            game_inf.selected_game_id = None

            return None


async def start_new_game(name):
    global game_inf
    json = await start_game_request(name)
    game_inf.selected_player = 1
    game_inf.selected_game_id = json['id']


async def start_game_request(name):
    global game_inf
    url = 'http://' + game_inf.host + ':' + str(game_inf.port) + '/start?name=' + str(name)
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url=url) as resp:
                if resp.status == 200:
                    try:
                        return await resp.json()
                    except:
                        pass
        except Exception as e:
            print(e)


async def get_games():
    global game_inf
    url = 'http://' + game_inf.host + ':' + str(game_inf.port) + '/list'
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url=url) as resp:
                return await resp.json()
        except Exception as e:
            print(e)
            return []


async def make_move(x, y):
    global game_inf
    json = await make_move_request(x, y)
    if json is not None:
        if not json['status'] == 'ok':
            print(json['message'])


async def make_move_request(x, y):
    global game_inf
    url = 'http://' + game_inf.host + ':' + str(game_inf.port) + '/play?game=' + str(game_inf.selected_game_id) + '&player=' + str(game_inf.selected_player) + '&x=' + str(x) + '&y=' + str(y)
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url=url) as resp:
                if resp.status == 200:
                    try:
                        return await resp.json()
                    except:
                        pass
        except Exception as e:
            print(e)


async def text_loop():
    global game_inf
    while game_inf.selected_game_id is None:
        try:
            games = await get_games()
            print('Type new to start a new game or type id of selected game to join the game')
            if len(games) > 0:
                print('Select game to join:')
                for item in games:
                    print('ID: ' + str(item['id']) + ' - ' + item['name'])
            else:
                print('no games to join')
            input_string = input()
            input_array = input_string.split(' ')
            if input_array[0] == 'new':
                if len(input_array) > 1:
                    name = ' '.join('%s' % item for item in input_array[1:])
                    await start_new_game(name)
                else:
                    await start_new_game('')
            else:
                if len([item for item in games if str(item['id']) == input_string]) > 0:
                    resp = await join_to_game(input_string)
                    if resp is not None:
                        print(resp)
                else:
                    print('This game is not listed')
            while game_inf.selected_game_id is not None:
                try:
                    await draw_board()
                    if game_inf.winner is not None:
                        if game_inf.winner != 0:
                            if game_inf.selected_player == game_inf.winner:
                                print('you win')
                            else:
                                print("you lose")
                        else:
                            print('draw')
                        game_inf.reset_game()
                    elif game_inf.next_player == game_inf.selected_player:
                        if game_inf.selected_player == 1:
                            game_symbol = 'X'
                        else:
                            game_symbol = 'O'
                        input_string = input('your turn (' + game_symbol + ')')
                        array = input_string.split(' ')
                        if len(array) == 2:
                            await make_move(array[0], array[1])
                        else:
                            print('cannot read x and y. Write two coordinates separated by space.')
                    await asyncio.sleep(1)
                except KeyboardInterrupt:
                    exit(0)
        except KeyboardInterrupt:
            exit(0)

def text_ui():
    if sys.platform.startswith('win'):
        loop = asyncio.ProactorEventLoop()
        asyncio.set_event_loop(loop)
    else:
        loop = asyncio.get_event_loop()
    loop.create_task(text_loop())
    loop.run_forever()


class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.text = text
        self.active = False

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))


def draw_symbol(board, boardRow, boardCol, player):
    centerX = (boardCol * 100) + 50
    centerY = (boardRow * 100) + 50

def position_on_board(mouseX, mouseY):
    if mouseY < 100:
        row = 0
    elif mouseY < 200:
        row = 1
    else:
        row = 2

    if mouseX < 100:
        col = 0
    elif mouseX < 200:
        col = 1
    else:
        col = 2

    return row, col

if __name__ == "__main__":
    if len(sys.argv) == 3:
        game_inf.host = (sys.argv[1])
        game_inf.port = (sys.argv[2])
        text_ui()

    else:
        print("Wrong number of arguments")
