# accounts/utils.py

import firebase_admin
from firebase_admin import credentials, storage
import os
from django.conf import settings
from urllib.parse import urlparse

def initialize_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate(os.path.join(settings.BASE_DIR, 'firebase_credentials.json'))
        firebase_admin.initialize_app(cred, {
            'storageBucket': settings.FIREBASE_CONFIG['storageBucket']
        })

def upload_profile_picture(user, file):
    initialize_firebase()
    
    bucket = storage.bucket()
    blob = bucket.blob(f'profile_pictures/{user.id}/{file.name}')
    blob.upload_from_file(file)
    blob.make_public()
    
    return blob.public_url

def delete_profile_picture(url):
    initialize_firebase()
    
    bucket = storage.bucket()
    parsed_url = urlparse(url)
    path = parsed_url.path.split('/o/')[-1].split('?')[0]
    blob = bucket.blob(path)
    blob.delete()