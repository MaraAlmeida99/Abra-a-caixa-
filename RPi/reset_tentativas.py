"""
 Faz reset do numero de tentativas a cada 5 minutos
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

try:
    while True:
        print("Reseting...")
        db.child("codigo").update({"num_tentativas": 0})
        time.sleep(300) # 300 == 5 minutes
except KeyboardInterrupt:
    exit()

