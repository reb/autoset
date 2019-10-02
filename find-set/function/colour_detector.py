import operator

import cv2
import numpy as np


def non_white_pixels(image):
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    (l, _, _) = cv2.split(lab)
    _, thresh = cv2.threshold(l, 180, 255, cv2.THRESH_BINARY)
    return cv2.bitwise_not(thresh)


def hue_to_colour(hue):
    if hue < 20:
        return 'R'
    if hue < 100:
        return 'G'
    return 'B'


def transform_point(point, width, height):
    return int(point['x'] * width), int(point['y'] * height)


def identify(image_data, bounding_box):
    # image = cv2.imread(image_data)
    image_data_array = np.asarray(bytearray(image_data), dtype=np.uint8)
    image = cv2.imdecode(image_data_array, cv2.IMREAD_COLOR)
    height, width, _ = image.shape
    top_left = transform_point(bounding_box['top_left'], width, height)
    bottom_right = transform_point(bounding_box['bottom_right'], width, height)
    card = image[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
    card_hsv = cv2.cvtColor(card, cv2.COLOR_BGR2HSV)
    mask = non_white_pixels(card)
    score = {'R': 0, 'G': 0, 'B': 0}
    for (image_row, mask_row) in zip(card_hsv, mask):
        for (image_px, mask_px) in zip(image_row, mask_row):
            if mask_px:
                colour = hue_to_colour(image_px[0])
                score[colour] += 1
    print(score)
    colour = max(score.items(), key=operator.itemgetter(1))[0]
    print(f'{top_left}, {bottom_right}: {colour}')
    return colour
