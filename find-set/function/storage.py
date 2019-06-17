import os
import string
import random
from datetime import datetime
from google.cloud import storage

STORAGE_CLIENT = storage.Client()
BUCKET_NAME = os.environ.get('BUCKET_NAME')


def upload(file_data):
    hash = ''.join(random.choice(string.ascii_lowercase) for _ in range(4))
    timestamp = str(datetime.now().strftime())

    bucket = STORAGE_CLIENT.get_bucket(BUCKET_NAME)
    blob = bucket.blob(f'{timestamp}-{hash}.jpg')

    blob.upload_from_string(file_data)
