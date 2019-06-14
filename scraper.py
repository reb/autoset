#!/usr/bin/python3

from urllib import request
from PIL import Image, ImageDraw


def add_corners(im, rad):
    circle = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)
    alpha = Image.new('L', im.size, 255)
    w, h = im.size
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
    im.putalpha(alpha)
    return im


i = 1
for fill in ['F', 'H', 'E']:
  for shape in ['W', 'D', 'P']:
    for color in ['R', 'B', 'G']:
      for count in [1, 2, 3]:
        tag = f'{count}{color}{fill}{shape}'
        print(f'Downloading {i}: {tag}...')
        request.urlretrieve(f'https://www.setgame.com/sites/all/modules/setgame_set/assets/images/new/{i}.png', f'cards/{tag}.png')
        card = Image.open(f'cards/{tag}.png').convert('RGBA').transpose(Image.ROTATE_90)
        add_corners(card, 15)
        card.save(f'cards/{tag}.png')
        i = i + 1
