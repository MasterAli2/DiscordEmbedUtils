import random
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont

import config


rows, cols = 6, 7


def playConnectFour(moves: list[str]):
    grid = [[0 for _ in range(rows)] for _ in range(cols)]
    past = []
    
    for i in moves:
        if not i.isdigit():
            continue
        i = int(i)
        
        if i < 1 or i > 7:
            continue
        
        if checkWin(grid, 1) or checkWin(grid, 2):
            grid = [[0 for _ in range(rows)] for _ in range(cols)]
        
        if not make_move(grid, i - 1, 1):
            break
            
        past.append(i)
        
        if checkWin(grid, 1):
            continue
            
        ai = ai_move(grid, hash(tuple(past)) + hash(i))
        if ai is not None:
            make_move(grid, ai, 2)
            
        if checkWin(grid, 2):
            continue
    
    return grid
        
        
def printBoard(board):
    for row in reversed(list(zip(*board))):
        print(" | ".join(str(x) for x in row))
        print("-" * (len(row) * 4 - 1))

        
def checkWin(board, side):
    for i in range(len(board)):
        for j in range(len(board[i])):
            side = board[i][j]
            if side == 0:
                continue
            
            if j + 3 < len(board[i]) and all(board[i][j + k] == side for k in range(4)):
                return side
            
            if i + 3 < len(board) and all(board[i + k][j] == side for k in range(4)):
                return side
            
            if i + 3 < len(board) and j + 3 < len(board[i]) and all(board[i + k][j + k] == side for k in range(4)):
                return side
    
    return None

def valid_moves(board):
    return [c for c in range(cols) if board[c][rows-1] == 0]

def make_move(board, col, piece):
    for r in range(rows):
        if board[col][r] == 0:
            board[col][r] = piece
            return True
    return False

def ai_move(board, seed):
    random.seed(hash(tuple(tuple(row) for row in board)) + hash(67) + hash(seed))
    
    for col in valid_moves(board):
        temp = [row[:] for row in board]
        make_move(temp, col, 2)
        if checkWin(temp, 2):
            return col
        
    for col in valid_moves(board):
        temp = [row[:] for row in board]
        make_move(temp, col, 1)
        if checkWin(temp, 1):
            return col
    return random.choice(valid_moves(board))



def drawConnectFour(board: list[list[int]], filename="connect_4.png"):
    size = 100
    width, height = cols * size, rows * size
    
    cell_width = width // cols
    cell_height = height // rows
    
    line_width = 5

    img = Image.new("RGB", (width, height+cell_height//2), "white")
    draw = ImageDraw.Draw(img)

    for i in range(0, rows+1):
        y = i * cell_height
        draw.line([(0, y), (width, y)], fill="black", width=line_width)

    for i in range(0, cols +1):
        x = i * cell_width
        draw.line([(x, 0), (x, height)], fill="black", width=line_width)

    for col in range(cols):
        for row in range(rows):
            val = board[col][row]
            if val != 0:
                x_center = col * cell_width + cell_width // 2
                y_center = (rows - 1 - row) * cell_height + cell_height // 2
                radius = min(cell_width, cell_height) // 2 - 5
                color = "red" if val == 1 else "yellow"
                draw.ellipse(
                    [(x_center - radius, y_center - radius),
                     (x_center + radius, y_center + radius)],
                    fill=color
                )

    font = ImageFont.truetype(config.FONT_PATH, cell_width // 3)

    for col in range(cols):
        text = str(col + 1)
        x_center = col * cell_width + cell_width // 2
        y_center = height + 75 - cell_height // 2
        bbox = draw.textbbox((0, 0), text, font=font)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text((x_center - w / 2, y_center - h / 2), text, fill="black", font=font)

    img_bytes = BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    return img_bytes