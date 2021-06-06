"""
 Escuta o num_tentativas no firebase, quando ultrapassa as 3 tentativas,
 emite o som de alerta
"""

import pyrebase
from firebase_admin import credentials
import os
import time

creds = credentials.Certificate("../log.json")
config = {
  "apiKey": "bwe43EWriuIQ045tl2fludU4l64T3OKwX8iQ03Sh",
  "authDomain": "abra-a-caixa.firebaseapp.com",
  "databaseURL": "https://abra-a-caixa-default-rtdb.europe-west1.firebasedatabase.app/",
  "storageBucket": "abra-a-caixa.appspot.com",
  "serviceAccount": "../log.json"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

def stream_handler(message):
    print(message["data"])
    if message["data"] >= 3:
        print("Alert!!!!")
        os.system("aplay alert.wav")

try:
    db.child("codigo").child("num_tentativas").stream(stream_handler)
except KeyboardInterrupt:
    stream.close()

