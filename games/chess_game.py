from __future__ import annotations

import chess
from stockfish import Stockfish

import chess.svg
from cairosvg import svg2png

import config

stockfish = Stockfish(path=config.STOCKFISH_PATH)
stockfish.set_skill_level(20)
    
    
def getNextState(uci :list[str]):
    board = chess.Board()
    stockfish.set_fen_position(board.fen())
    j = 0
    for i in uci: 
        j += 1
        try:
            move = board.parse_san(i)
            board.push(move)
            
            stockfish.set_fen_position(board.fen())
            
            best_move_uci = stockfish.get_best_move()
            if best_move_uci:
                board.push_uci(best_move_uci)
                
        except chess.IllegalMoveError:
            continue
        except chess.InvalidMoveError:
            continue
    
    return board.fen()

def fen_to_png(fen: str):
    board = chess.Board(fen)
    board_svg = chess.svg.board(board=board, size=350)
    return svg2png(bytestring=board_svg.encode("utf-8"))