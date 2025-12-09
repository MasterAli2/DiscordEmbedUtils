import random
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont

import config

MINE_PERCENTAGE = 0.21
SIZE = 10


def playMineSweeper(moves):
    moves = split_letter_number_pairs(moves)
    
    past = []
    first_move = True
    
    board = [["N" for _ in range(SIZE)] for _ in range(SIZE)]

    for i in moves:
        if i[0] < 0 or i[0] > SIZE or i[1] < 0 or i[1] > SIZE:
            print("Illegal move")
            continue
        
        if (board[i[0]-1][i[1]-1]).endswith("+"):
            print("Illegal move")
            continue
        
        past.append(i)
        
        if first_move:
            board = [["N" for _ in range(SIZE)] for _ in range(SIZE)]
            
            x= i[0]-1
            y= i[1]-1
            place_mines(board, x, y, hash(tuple(past)))
            place_numbers(board)
        
        play = uncover(board, i[0]-1, i[1]-1, is_first=True, real_first=first_move)
        if play == "M":
            print("Game Over")
            first_move = True
            continue
        
        if checkWin(board):
            print("You Win!")
            first_move = True
            continue
        
        first_move = False
        
    return board

def checkWin(board):
    for i in board:
        for j in i:
            if j == "M":
                continue
            if not j.endswith("+"):
                return False
    return True

def applyLoss(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == "M":
                board[i][j] = "M+"
    return board
            
def uncover(board, x, y, depth: int = 0, is_first :bool = False, real_first: bool = False):
    if board[x][y] == "M":
        applyLoss(board)
        return "M"
    elif (board[x][y]) == "0" and not (board[x][y]).endswith("+") or (real_first and is_first):
        board[x][y] = f"{str(board[x][y])}+"
        
        if board[x][y] == "0+":
            depth = 0
        else:
            depth += 1
        
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(board) and 0 <= ny < len(board[0]) and board[nx][ny] != "M":
                    print("Recursing to", nx, ny)
                    uncover(board, nx, ny, depth= depth)
    elif not board[x][y].endswith("+"):
        board[x][y] = f"{board[x][y]}+" 
    return board[x][y]
            
def place_mines(board, first_x, first_y, seed):
    random.seed(hash(seed) + hash(first_x^2+first_y^2 + hash(seed)))
    
    total_cells = len(board) * len(board[0])
    num_mines = int(total_cells * MINE_PERCENTAGE)
    mines_placed = 0
    attempts = 0
    max_attempts = total_cells * 11

    while mines_placed < num_mines:
        if attempts > max_attempts:
            break
        
        x = random.randint(0, len(board) - 1)
        y = random.randint(0, len(board[0]) - 1)

        if (x, y) != (first_x, first_y) and board[x][y] != 'M':
            board[x][y] = "M"
            mines_placed += 1
                        
        attempts += 1
        
def place_numbers(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            neighboring_mines = 0
            
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx, ny = i + dx, j + dy
                    if 0 <= nx < len(board) and 0 <= ny < len(board[0]) and board[nx][ny] == 'M':
                        neighboring_mines += 1
            if board[i][j] != 'M':            
                board[i][j] = str(neighboring_mines)
            
    return board
    
def printBoard(board):
    for row in reversed(list(zip(*board))):
        print(" | ".join(str(x) for x in row))
        print("-" * (len(row) * 4 - 1))
    
def split_letter_number_pairs(input_string: str) -> list[tuple[int, int]]:
    result = []
    i = 0
    n = len(input_string)
    input_string = input_string.lower()
    
    while i < n:
        if input_string[i].isalpha():
            if i + 1 < n and input_string[i + 1].isdigit():
                letter = input_string[i]
                i += 1
                
                number_str = ""
                while i < n and input_string[i].isdigit():
                    number_str += input_string[i]
                    i += 1
                    
                number = (int(number_str))  
                result.append(tuple([ord(letter)-96, int(number)]))
            else:
                i += 1
        else:
            i += 1
    
    return result


def drawMS(board: list[list[int]]):
    size = 100
    width, height = SIZE * size, SIZE * size
    
    cell_width = width // SIZE
    cell_height = height // SIZE
    
    line_width = 5
    font = ImageFont.truetype(config.FONT_PATH, cell_width // 3)
    

    img = Image.new("RGB", (width+cell_width//2, height+cell_height//2), "white")
    draw = ImageDraw.Draw(img)

    for i in range(0, SIZE+1):
        y = i * cell_height
        draw.line([(0, y), (width, y)], fill="black", width=line_width)

    for i in range(0, SIZE +1):
        x = i * cell_width
        draw.line([(x, 0), (x, height)], fill="black", width=line_width)

    for col in range(SIZE):
        for row in range(SIZE):
            val = board[col][row]
            if True:
                x_center = col * cell_width + cell_width // 2
                y_center = (SIZE - 1 - row) * cell_height + cell_height // 2
                radius = min(cell_width, cell_height) // 2 - 5
                color = "red" if val == "M+" else ("green" if val.endswith("+") else "gray")
                draw.ellipse(
                    [(x_center - radius, y_center - radius),
                     (x_center + radius, y_center + radius)],
                    fill=color
                )

                if val.endswith("+"):
                    bbox = draw.textbbox((0, 0), val.removesuffix("+"), font=font)
                    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
                    draw.text((x_center - w / 2, y_center - h / 2), val.removesuffix("+"), fill="black", font=font)


    for col in range(10):
        text = str(chr(col + 97))
        x_center = col * cell_width + cell_width // 2
        y_center = height + 75 - cell_height // 2
        bbox = draw.textbbox((0, 0), text, font=font)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text((x_center - w / 2, y_center - h / 2), text, fill="black", font=font)
        
        text = str(11-(col+1))
        x_center = height + 75 - cell_width // 2
        y_center = col * cell_height + cell_height // 2
        bbox = draw.textbbox((0, 0), text, font=font)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text((x_center - w / 2, y_center - h / 2), text, fill="black", font=font)

    img_bytes = BytesIO()
    img.resize([SIZE*10, SIZE*10])
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    return img_bytes