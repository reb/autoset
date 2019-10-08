import base64
import json
import os
from itertools import combinations
import requests
import storage
import colour_detector

PREDICTION_URL = os.environ.get('PREDICTION_URL')


def get_predictions(image_bytes, image_key):
    instances = {
        'instances': [
            {'image_bytes': {'b64': image_bytes},
             'key': image_key}
        ]
    }

    response = requests.post(PREDICTION_URL, data=json.dumps(instances))
    response_json = response.json()
    result = response_json['predictions'][0]

    predictions = []
    for i in range(int(result['num_detections'])):
        if result['detection_scores'][i] > 0.5:
            name = result['detection_classes_as_text'][i]
            bounding_box = result['detection_boxes'][i]
            predictions.append({
                "name": name,
                "bounding_box": {
                    "top_left": {
                        "y": bounding_box[0],
                        "x": bounding_box[1]
                    },
                    "bottom_right": {
                        "y": bounding_box[2],
                        "x": bounding_box[3]
                    }
                }
            })
    return predictions


def handle(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    if request.method == 'OPTIONS':
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }
        return '', 204, headers

    execution_id = request.headers.get("Function-Execution-Id")

    # Set CORS headers for the main request
    headers = {
        'Access-Control-Allow-Origin': '*'
    }

    request_json = request.get_json()
    image = request_json.get('image')
    image_bytes = base64.b64decode(image.encode())
    storage.upload(image_bytes, execution_id)
    predictions = get_predictions(image, execution_id)
    log_predictions(predictions)

    coloured = identify_colours_with_kmeans(image_bytes, predictions)
    found_set = find_set(coloured)
    response = json.dumps(found_set)
    return response, 200, headers


def identify_colours(image_bytes, cards):
    for card in cards:
        colour = colour_detector.identify(image_bytes, card['bounding_box'])
        card['name'] = card['name'][0] + colour + card['name'][1:]
    return cards


def identify_colours_with_kmeans(image_bytes, cards):
    bounding_boxes = [card['bounding_box'] for card in cards]
    colours = colour_detector.identify_all_with_kmeans(image_bytes, bounding_boxes)
    for card, colour in zip(cards, colours):
        card['name'] = card['name'][0] + colour + card['name'][1:]


def find_set(cards):
    for potential_set in combinations(cards, 3):
        if is_set(*[c['name'] for c in potential_set]):
            return potential_set
    return []


def is_set(a, b, c):
    for f_a, f_b, f_c in zip(a, b, c):
        all_same = f_a == f_b == f_c
        all_different = f_a != f_b != f_c != f_a
        if not (all_same or all_different):
            return False
    return True


def log_predictions(predictions):
    print("Found bounding boxes:")
    for prediction in predictions:
        print(prediction)
