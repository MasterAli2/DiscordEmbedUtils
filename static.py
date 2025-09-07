from PIL import Image, ImageDraw, ImageFont
import os

import config


def drawText(text: str, filename, font_size=100):
    width, height = 350, 350
    line_width = 5

    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)
    
    font = ImageFont.truetype(config.FONT_PATH, font_size)
    
    bbox = draw.textbbox((0, 0), text, font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(((width-w)//2, (height-h)//2), text, fill="black", font=font)
    
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))
    
    img.save(filename, format='PNG')
    return img

def main():
    drawText("Hello", "static/hello.png", font_size=100)
    drawText("Game Not Found", "static/game_not_found.png", font_size=40)
    drawText("404, Not Found", "static/err/404.png", font_size=100)
    drawText("oops\n500", "static/err/500.png", font_size=100)
    print("Done")
    
if __name__ == "__main__":
    main()