import os
import base64
from itertools import combinations
from google.cloud import automl_v1beta1

PROJECT_ID = os.environ.get('PROJECT_ID')
MODEL_ID = os.environ.get('MODEL_ID')


# 'content' is base-64-encoded image data.
def get_prediction(content):
    client = automl_v1beta1.PredictionServiceClient()
    content = base64.b64decode(content.encode())

    name = f'projects/{PROJECT_ID}/locations/us-central1/models/{MODEL_ID}'
    payload = {'image': {'image_bytes': content}}
    params = {}
    request = client.predict(name, payload, params)
    return request  # waits till request is returned


def handle(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """

    request_json = request.get_json()
    image = request_json.get('image')
    prediction = get_prediction(image)
    set = find_set(prediction)
    return set


def find_set(prediction):
    for potential_set in combinations(prediction.payload, 3):
        if is_set(*[c.display_name for c in potential_set]):
            return potential_set
    return None


def is_set(a, b, c):
    for f_a, f_b, f_c in zip(a, b, c):
        # feature is all the same
        if f_a == f_b == f_c:
            continue
        # feature is all different
        if f_a != f_b != f_c != f_a:
            continue
        # this is not a set
        return False
    return True

