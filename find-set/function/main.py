import os
import base64
import json
from itertools import combinations
from google.cloud import automl_v1beta1
from colour_detector import identify

PROJECT_ID = os.environ.get('PROJECT_ID')
MODEL_ID = os.environ.get('MODEL_ID')


# 'content' is base-64-encoded image data.
def get_prediction(image_bytes):
    client = automl_v1beta1.PredictionServiceClient()

    name = f'projects/{PROJECT_ID}/locations/us-central1/models/{MODEL_ID}'
    payload = {'image': {'image_bytes': image_bytes}}
    params = {}
    response = client.predict(name, payload, params)
    return response  # waits till request is returned


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

    # Set CORS headers for the main request
    headers = {
        'Access-Control-Allow-Origin': '*'
    }

    request_json = request.get_json()
    image = request_json.get('image')
    image_bytes = base64.b64decode(image.encode())
    prediction = get_prediction(image_bytes)
    log_prediction(prediction)

    coloured = identify_colours(image_bytes, prediction.payload)
    found_set = find_set(coloured)
    response = json.dumps([format_annotation(card) for card in found_set])
    return response, 200, headers


def identify_colours(image_bytes, cards):
    for card in cards:
        colour = identify(image_bytes, card.image_object_detection.bounding_box.normalized_vertices)
        card.display_name = card.display_name[0] + colour + card.display_name[1:]
    return cards


def find_set(cards):
    for potential_set in combinations(cards, 3):
        if is_set(*[c.display_name for c in potential_set]):
            return potential_set
    return []


def is_set(a, b, c):
    for f_a, f_b, f_c in zip(a, b, c):
        all_same = f_a == f_b == f_c
        all_different = f_a != f_b != f_c != f_a
        if not (all_same or all_different):
            return False
    return True


def format_annotation(annotation):
    bounding_box = annotation.image_object_detection.bounding_box.normalized_vertices
    return {
        "name": annotation.display_name,
        "bounding_box": [format_point(p) for p in bounding_box]
    }


def format_point(point):
    return {
        "x": point.x,
        "y": point.y
    }


def log_prediction(prediction):
    print("Found bounding boxes:")
    for annotation in prediction.payload:
        bbox = annotation.image_object_detection.bounding_box.normalized_vertices
        print(f'{bbox[0].x},{bbox[0].y},{bbox[1].x},{bbox[1].y},{annotation.display_name}')
