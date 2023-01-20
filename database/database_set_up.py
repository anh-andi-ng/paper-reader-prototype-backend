import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import firestore

class Database:

    def __init__(self, cred: str, firebase_url: str):
        self.cred = credentials.Certificate(cred)
        self.firebase_admin =  firebase_admin.initialize_app(
                self.cred, {'databaseURL': firebase_url})
        self.db = firestore.client()

    def __str__(self):
        return f"{self.db}"

    
