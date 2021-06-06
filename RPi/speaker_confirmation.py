"""
    Abre a caixa
    Emite um som de confirmação e um sinal de luz verde quando a caixa está aberta
    Emite um sinal de luz vermelho quando caixa está fechada
    Faz update do estado.
"""

import pyrebase
from firebase_admin import credentials
import os
import time
import serial, string
import RPi.GPIO as GPIO

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

ser = serial.Serial("/dev/ttyACM0", 9600, 8, 'N', 1, timeout=1)

# pin definitions
redPin = 17
greenPin = 23

# setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(redPin, GPIO.OUT)
GPIO.setup(greenPin, GPIO.OUT)

def stream_handler(message):
	print(message["data"])
	if message["data"] == "Aberto":
		ser.write(b"RASPBERRY OPEN\n")
		os.system("aplay confirmation.wav")
		GPIO.output(redPin, GPIO.LOW)
		GPIO.output(greenPin, GPIO.HIGH)
	else:
		ser.write(b"RASPBERRY CLOSE\n")
		GPIO.output(redPin, GPIO.HIGH)
		GPIO.output(greenPin, GPIO.LOW)

try:
	db.child("estado").stream(stream_handler)
except KeyboardInterrupt:
	stream.close()
	GPIO.cleanup()
