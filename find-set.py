#!/usr/bin/python3

from urllib import request
import sys
import base64
import json
from PIL import Image, ImageDraw


def show_bbs(image_file, cards):
    image = Image.open(image_file)
    # [{'name': '1ED', 'bounding_box': [{'x': 0.24633699655532837, 'y': 0.6990789771080017}, {'x': 0.32551199197769165, 'y': 0.9871280193328857}]}, {'name': '2EW', 'bounding_box': [{'x': 0.4516269862651825, 'y': 0.1058880016207695}, {'x': 0.5277140140533447, 'y': 0.3374119997024536}]}, {'name': '3EP', 'bounding_box': [{'x': 0.5745459794998169, 'y': 0.6790819764137268}, {'x': 0.6538180112838745, 'y': 0.9584609866142273}]}]

    draw = ImageDraw.Draw(image)

    for card in cards:
        bb = card['bounding_box']
        top_left = (bb[0]['x'] * image.size[0], bb[0]['y'] * image.size[1])
        bottom_right = (bb[1]['x'] * image.size[0], bb[1]['y'] * image.size[1])
        draw.rectangle([
            top_left,
            bottom_right
        ], None, (255, 0, 0), width = 3)

    image.show()


if __name__ == '__main__':
    image_file = sys.argv[1]
    with open(image_file, 'rb') as image_data:
        image = str(base64.b64encode(image_data.read()), 'utf-8')
        req = request.Request('https://europe-west1-strong-jetty-243820.cloudfunctions.net/find-set')
        req.add_header('Content-Type', 'application/json; charset=utf-8')
        json_data = json.dumps({'image': image})
        json_data_as_bytes = json_data.encode('utf-8')
        req.add_header('Content-Length', len(json_data_as_bytes))
        response = request.urlopen(req, json_data_as_bytes)
        found_set = json.loads(response.read())
        print(found_set)
        if found_set:
            print('Found a set! 😺')
            show_bbs(image_file, found_set)
        else:
            print('No set found 😞')

