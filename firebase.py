# firebase.py

import firebase_admin
from firebase_admin import credentials, firestore

# Chemin vers votre fichier de configuration JSON fourni par Firebase
FIREBASE_CONFIG_JSON = 'ecg-arduino-firebase-adminsdk-2lbdy-f3ffad2926.json'

# Initialisation de Firebase avec votre fichier de configuration JSON
cred = credentials.Certificate(FIREBASE_CONFIG_JSON)
firebase_admin.initialize_app(cred)

# Accès à Firestore
db = firestore.client()

def get_firestore():
    return db
