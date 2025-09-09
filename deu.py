from flask import Flask, send_file, request
from flask_caching import Cache
import io

from games.chess_game import fen_to_png, getNextState
from games.tiktaktoe_game import getBoard, drawTikTakToe
from games.connect4_game import drawConnectFour, playConnectFour
from games.minesweeper_game import drawMS, playMineSweeper

import utils as utilities

import config

app = Flask(__name__)
app.config.from_mapping(config.CACH_CONFIG)
cache = Cache(app)


@app.route('/games/<string:game>/<string:san>', strict_slashes=False)
@utilities.discord_only
@cache.cached()
def games(game: str, san: str):
    if san.endswith(config.APPENDING_SUFFIX):
        san = san.removesuffix(config.APPENDING_SUFFIX)

    if game == "chess":
        moves = san.split('.')
        fen = getNextState(moves)
        file = fen_to_png(fen)
        buffer = io.BytesIO(file)
        buffer.seek(0)
    elif game == "four":
        moves = list(san)
        fen = playConnectFour(moves)
        buffer = drawConnectFour(fen)
    elif game == "ttt":
        moves = list(san)
        board = getBoard(moves)
        buffer = drawTikTakToe(board)
    elif game == "ms":
        moves = san
        fen = playMineSweeper(moves)
        buffer = drawMS(fen)
    else:
        return send_file("static/game_not_found.png", mimetype='image/png')

    return send_file(buffer, mimetype='image/png')
    

@app.route('/')
@utilities.discord_only
def index():
    return send_file("static/hello.png", mimetype='image/png')


@app.before_request
def before_request():
    pass


@app.errorhandler(404)
def page_not_found(e):
    return send_file("static/err/404.png", mimetype='image/png'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return send_file("static/err/500.png", mimetype='image/png'), 500

