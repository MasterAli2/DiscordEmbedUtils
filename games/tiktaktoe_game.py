import random

from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

import config

def getBoard(move: list[str]):
    difficulty = "medium"
    past = []
    board = [f"{i + 1}" for i in range(9)]
    
    for i in move:
        if not i.isdigit():
            print("Invalid move")
            continue
        i = int(i)
        
        if len(board) < i or i < 1:
            print("Illegal move")
            continue
        past.append(i)
        
        if check_winner(board):
            board = [f"{i + 1}" for i in range(9)]
        
        if board[i - 1] in ['X', 'O']:
            print("Illegal move")
            break
        
        board[i - 1] = 'X'
        
        ai = ai_move(board, hash(tuple(past)) + hash(i), difficulty)
        if ai is not None:
            board[ai] = 'O'
        
        if check_winner(board):
            print(f"{check_winner(board)} wins!")
            continue
    
    return board


def check_winner(board):
    lines = [
        (0,1,2), (3,4,5), (6,7,8),
        (0,3,6), (1,4,7), (2,5,8),
        (0,4,8), (2,4,6)
    ]
    for a,b,c in lines:
        if board[a] == board[b] == board[c] and board[a] in ["X", "O"]:
            return board[a]
    return None

def empty_cells(board):
    return [i for i, x in enumerate(board) if x.isdigit()]

def minimax(board, is_maximizing):
    winner = check_winner(board)
    if winner == "O":
        return 1
    elif winner == "X":
        return -1
    elif not empty_cells(board):
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for i in empty_cells(board):
            board[i] = "O"
            score = minimax(board, False)
            board[i] = str(i + 1)
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in empty_cells(board):
            board[i] = "X"
            score = minimax(board, True)
            board[i] = str(i + 1)
            best_score = min(score, best_score)
        return best_score

def best_move(board, seed):
    random.seed(hash(tuple(board)) + hash(67) + hash(seed))
    
    best_score = -float('inf')
    move = None
    for i in empty_cells(board):
        board[i] = "O"
        score = minimax(board, False)
        board[i] = str(i + 1)
        if score > best_score:
            best_score = score
            move = i
            
    if move is None and len(empty_cells(board)) > 0:
        return random.choice(empty_cells(board))
    
    return move

def ai_move(board, seed, difficulty="hard"):
    random.seed(hash(tuple(board)) + hash(difficulty) + hash(seed))
    
    if difficulty == "easy":
        return random.choice(empty_cells(board))
    elif difficulty == "medium":
        if random.random() < 0.5:
            return best_move(board, seed)
        else:
            return random.choice(empty_cells(board))
    else:
        return best_move(board, seed)
    
def drawTikTakToe(board: list[str], filename="tictactoe.png"):
    size = 300
    cell = size // 3
    line_width = 5
    img = Image.new("RGB", (size, size), "white")
    draw = ImageDraw.Draw(img)

    for i in range(1, 3):
        draw.line([(i*cell, 0), (i*cell, size)], fill="black", width=line_width)
        draw.line([(0, i*cell), (size, i*cell)], fill="black", width=line_width)

    font1 = ImageFont.truetype(config.FONT_PATH, 50)
    font2 = ImageFont.truetype(config.FONT_PATH, 22)

    for i, val in enumerate(board):
        if val.upper() in ["X", "O"]:
            x = (i % 3) * cell + cell // 2
            y = (i // 3) * cell + cell // 2
            bbox = draw.textbbox((0, 0), val, font=font1)
            w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
            draw.text((x - w/2, y - h/2), val, fill="black", font=font1)
        else:
            x = (i % 3) * cell + cell // 2
            y = (i // 3) * cell + cell // 2
            bbox = draw.textbbox((0, 0), val, font=font2)
            w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
            draw.text((x - w/2, y - h/2), val, fill="gray", font=font2)

    img_bytes = BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    return img_bytes
    
if __name__ == "__main__":
    a = (getBoard("hard", ["2", "5", "3", "4"]))
    print(a)
    drawTikTakToe(a, "atik.png")