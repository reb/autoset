import os
from datetime import datetime
from google.cloud import storage

STORAGE_CLIENT = None
BUCKET_NAME = os.environ.get('BUCKET_NAME')


def upload(file_data, hash):
    global STORAGE_CLIENT
    if STORAGE_CLIENT is None:
        STORAGE_CLIENT = storage.Client()

    timestamp = datetime.now().strftime("%Y-%m-%d %H%M%S.%f")

    bucket = STORAGE_CLIENT.get_bucket(BUCKET_NAME)
    blob = bucket.blob(f'{timestamp}-{hash}.jpg')

    blob.upload_from_string(file_data)
