import operator

from sklearn.cluster import KMeans
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
    return {
        'x': int(point['x'] * width),
        'y': int(point['y'] * height),
    }


def average_pixel(image, bounding_box):
    height, width, _ = image.shape
    top_left = transform_point(bounding_box['top_left'], width, height)
    bottom_right = transform_point(bounding_box['bottom_right'], width, height)
    card = image[top_left['y']:bottom_right['y'], top_left['x']:bottom_right['x']]
    card_hsv = cv2.cvtColor(card, cv2.COLOR_BGR2HSV)
    mask = non_white_pixels(card)
    return cv2.mean(card_hsv, mask=mask)


def identify(image_data, bounding_box):
    image_data_array = np.asarray(bytearray(image_data), dtype=np.uint8)
    image = cv2.imdecode(image_data_array, cv2.IMREAD_COLOR)
    height, width, _ = image.shape
    top_left = transform_point(bounding_box['top_left'], width, height)
    bottom_right = transform_point(bounding_box['bottom_right'], width, height)
    card = image[top_left['y']:bottom_right['y'], top_left['x']:bottom_right['x']]
    card_hsv = cv2.cvtColor(card, cv2.COLOR_BGR2HSV)
    mask = non_white_pixels(card)
    score = {'R': 0, 'G': 0, 'B': 0}
    for (image_row, mask_row) in zip(card_hsv, mask):
        for (image_px, mask_px) in zip(image_row, mask_row):
            if mask_px:
                colour = hue_to_colour(image_px[0])
                score[colour] += 1
    colour = max(score.items(), key=operator.itemgetter(1))[0]
    return colour


def identify_all_with_kmeans(image_data, bounding_boxes):
    average_pixels = []
    for bounding_box in bounding_boxes:
        image_data_array = np.asarray(bytearray(image_data), dtype=np.uint8)
        image = cv2.imdecode(image_data_array, cv2.IMREAD_COLOR)
        average_pixels.append(average_pixel(image, bounding_box))

    previous_gap = 0
    for k in [1, 2, 3]:
        # To determine the optimal amount of clusters use the Gap Statistic
        # from Tibshirani, Walther, Hastie

        # First create a reference dispersion from random samples
        sample_dispersions = []
        for i in range(10):
            sample = np.random.random_sample(size=(len(average_pixels), len(average_pixels[0])))
            sample *= 255
            km = KMeans(k)
            km.fit(sample)
            sample_dispersions.append(km.inertia_)
        reference_dispersion = np.mean(sample_dispersions)

        # Then fit the average pixels
        km = KMeans(k)
        km.fit(average_pixels)
        dispersion = km.inertia_
        print(f"Reference: {reference_dispersion} Actual: {dispersion}")
        gap = np.log(reference_dispersion) - np.log(dispersion)
        print(f"Gap: {gap}")
        if gap < previous_gap:
            return translate_labels(km.labels_)
        previous_gap = gap

    # return the labels for the maximum amount of clusters
    return translate_labels(km.labels_)


def translate_labels(k_mean_labels):
    return [translate_to_readable_label(label) for label in k_mean_labels]


def translate_to_readable_label(k_mean_label):
    if k_mean_label == 0:
        return '#'
    if k_mean_label == 1:
        return '*'
    if k_mean_label == 2:
        return '+'
    return '?'
