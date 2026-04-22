import firebase_admin
from firebase_admin import credentials,firestore, auth
from app.config import settings

cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS)
# firebase_app = firebase_admin.initialize_app(cred)
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()
firebase_auth = auth
