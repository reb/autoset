#!/usr/bin/python3

from PIL import Image, ImageFilter
import random
import math
import numpy

cards = [(f'1{color}FW', Image.open(f'cards/1{color}FW.png')) for color in ['R', 'G', 'B']]
SIZE = 512
TARGET_SIZE = 512


def find_coeffs(pa, pb):
    matrix = []
    for p1, p2 in zip(pa, pb):
        matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0]*p1[0], -p2[0]*p1[1]])
        matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1]*p1[0], -p2[1]*p1[1]])

    A = numpy.matrix(matrix, dtype=numpy.float)
    B = numpy.array(pb).reshape(8)

    res = numpy.dot(numpy.linalg.inv(A.T * A) * A.T, B)
    return numpy.array(res).reshape(8)


def transform_image(img):
    width, height = img.size
    quarterWidth = int(width / 4)
    quarterHeight = int(height / 4)
    goal = [
            (random.randint(0, quarterWidth), random.randint(0, quarterHeight)),
            (random.randint(width - quarterWidth, width), random.randint(0, quarterHeight)),
            (random.randint(width - quarterWidth, width), random.randint(height - quarterHeight, height)),
            (random.randint(0, quarterWidth), random.randint(height - quarterHeight, height))
    ]

    coeffs = find_coeffs(
            goal,
        [
            (0, 0),
            (width, 0),
            (width, height),
            (0, height)
        ]
    )

    perspectified = img.transform((width, height), Image.PERSPECTIVE, coeffs, Image.BICUBIC)
    cardSize = 200
    # resized = perspectified.resize((cardSize, int(cardSize * perspectified.size[1] / perspectified.size[0])), Image.BICUBIC)
    return perspectified, goal


def convert_to_relative(boundingBox, location, imageSize):
    return [convert_point(p, location, imageSize) for p in boundingBox]


def convert_point(point, location, imageSize):
    x, y = point
    locationX, locationY = location
    width, height = imageSize
    return ((x + locationX) / width, (y + locationY) / height)


def render_background(img):
    center = (random.randrange(0, SIZE), random.randrange(0, SIZE))
    innerColor = [random.randrange(0, 256), random.randrange(0, 256), random.randrange(0, 256)]
    outerColor = [random.randrange(0, 256), random.randrange(0, 256), random.randrange(0, 256)]
    for y in range(SIZE):
        for x in range(SIZE):
            distanceToCenter = math.sqrt((x - center[0]) ** 2 + (y - center[1]) ** 2)
            normalizedDistanceToCenter = float(distanceToCenter) / (math.sqrt(2) * SIZE / 2)
            r = outerColor[0] * normalizedDistanceToCenter + innerColor[0] * (1 - normalizedDistanceToCenter)
            g = outerColor[1] * normalizedDistanceToCenter + innerColor[1] * (1 - normalizedDistanceToCenter)
            b = outerColor[2] * normalizedDistanceToCenter + innerColor[2] * (1 - normalizedDistanceToCenter)
            img.putpixel((x, y), (int(r), int(g), int(b)))


def generate(id, cardIndex, csv_file):
    print(id)
    output = Image.new('RGB', (SIZE, SIZE))
    render_background(output)

    # put down some cards
    card = cards[cardIndex][1]
    tag = cards[cardIndex][0]

    # cardToPlace = card.resize((cardSize, int(cardSize * card.size[1] / card.size[0])), Image.BICUBIC).rotate(random.randint(0, 360), expand=1)
    # for y in range(3):
    #   for x in range(3):

    cardToPlace, boundingBox = transform_image(card)

    output.paste(cardToPlace, (random.randint(0, SIZE - cardToPlace.size[0]), random.randint(0, SIZE - cardToPlace.size[1])), cardToPlace)

    output.filter(ImageFilter.GaussianBlur(random.randint(1, 4))).save(f'training-set/{id}.png')

    csv_file.write(f'gs://autoset-vcm/generated/{id}.png,{tag}\n')


random.seed(42)
with open('training-set/_tags.csv', 'w') as csv_file:
    for cardIndex in range(len(cards)):
        for i in range(101):
            generate(f'{cardIndex}-{i}', cardIndex, csv_file)
