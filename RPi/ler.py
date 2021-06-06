#!/usr/bin/python3

import serial, string, time
import pyrebase
from firebase_admin import credentials

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
ser1 = serial.Serial("/dev/ttyACM1", 9600, 8, 'N', 1, timeout=1)

# definir ordem:
ord_cod_bat = "1"
ord_cod_num = "2"
ord_cod_rot = "3"

""" output format
KEYPAD 1234
JOYSTICK UDRL
TOUCHPAD SLLS
"""

estado = "Fechada"
partes_corretas = ""
n_tentativas = 0
while True:
    output = ser.readline()
    output1 = ser1.readline()
    
    if (output == b'CLOSE\r\n') | (output1 == b'CLOSE\r\n'):
        db.update({"estado": "Fechado"})
        output = b''
        output1 = b''

    if (output != b'') | (output1 != b''):
        if output != b'':
            tipo = output.split()[0]
            cod = output.split()[1]
        else:
            tipo = output1.split()[0]
            cod = output1.split()[1]
        print(tipo)
        print(cod)        
        partes_corretas = db.child("codigo").child("partes_corretas").get().val()
        n_tentativas = db.child("codigo").child("num_tentativas").get().val()
        if tipo == b"KEYPAD":
            codigo_db = db.child("chave").child("codigo_numerico").get().val()
            if cod.decode('utf-8') == codigo_db:
                ordem_db = db.child("chave").child("codigo_ordem").get().val()
                if ordem_db[0] == ord_cod_num:
                    db.child("codigo").update({"partes_corretas": ord_cod_num})
                elif ordem_db[1] == ord_cod_num:
                    if len(partes_corretas) == 1:
                        db.child("codigo").update({"partes_corretas": partes_corretas+ord_cod_num})
                    else:
                        db.child("codigo").update({"num_tentativas": n_tentativas+1})
                        db.child("codigo").update({"partes_corretas": ""})
                elif ordem_db[2] == ord_cod_num:
                    if len(partes_corretas) == 2:
                        db.child("codigo").update({"partes_corretas": partes_corretas+ord_cod_num})
                        db.update({"estado": "Aberto"})
                        db.child("codigo").update({"partes_corretas": ""})
                    else:
                        db.child("codigo").update({"num_tentativas": n_tentativas+1})
                        db.child("codigo").update({"partes_corretas": ""})
                else:
                    db.child("codigo").update({"num_tentativas": n_tentativas+1})
                    db.child("codigo").update({"partes_corretas": ""})
            else:
                db.child("codigo").update({"num_tentativas": n_tentativas+1})
                db.child("codigo").update({"partes_corretas": ""})
                n_tentativas += 1
                partes_corretas = ""

        elif tipo == b"JOYSTICK":
            codigo_db = db.child("chave").child("codigo_rotacoes").get().val()
            if cod.decode('utf-8') == codigo_db:
                ordem_db = db.child("chave").child("codigo_ordem").get().val()
                if ordem_db[0] == ord_cod_rot:
                    db.child("codigo").update({"partes_corretas": ord_cod_rot})
                elif ordem_db[1] == ord_cod_rot:
                    if len(partes_corretas) == 1:
                        db.child("codigo").update({"partes_corretas": partes_corretas+ord_cod_rot})
                    else:
                        db.child("codigo").update({"num_tentativas": n_tentativas+1})
                        db.child("codigo").update({"partes_corretas": ""})
                elif ordem_db[2] == ord_cod_rot:
                    if len(partes_corretas) == 2:
                        db.child("codigo").update({"partes_corretas": partes_corretas+ord_cod_rot})
                        db.update({"estado": "Aberto"})
                        db.child("codigo").update({"partes_corretas": ""})
                    else:
                        db.child("codigo").update({"num_tentativas": n_tentativas+1})
                        db.child("codigo").update({"partes_corretas": ""})
                else:
                    db.child("codigo").update({"num_tentativas": n_tentativas+1})
                    db.child("codigo").update({"partes_corretas": ""})
            else:
                db.child("codigo").update({"num_tentativas": n_tentativas+1})
                db.child("codigo").update({"partes_corretas": ""})
        else:
            codigo_db = db.child("chave").child("codigo_batidas").get().val()

            if cod.decode('utf-8') == codigo_db:
                ordem_db = db.child("chave").child("codigo_ordem").get().val()
                if ordem_db[0] == ord_cod_bat:
                    db.child("codigo").update({"partes_corretas": ord_cod_bat})
                elif ordem_db[1] == ord_cod_bat:
                    if len(partes_corretas) == 1:
                        db.child("codigo").update({"partes_corretas": partes_corretas+ord_cod_bat})
                    else:
                        db.child("codigo").update({"num_tentativas": n_tentativas+1})
                        db.child("codigo").update({"partes_corretas": ""})
                elif ordem_db[2] == ord_cod_bat:
                    if len(partes_corretas) == 2:
                        db.child("codigo").update({"partes_corretas": partes_corretas+ord_cod_bat})
                        db.update({"estado": "Aberto"})
                        db.child("codigo").update({"partes_corretas": ""})
                    else:
                        db.child("codigo").update({"num_tentativas": n_tentativas+1})
                        db.child("codigo").update({"partes_corretas": ""})
                else:
                    db.child("codigo").update({"num_tentativas": n_tentativas+1})
                    db.child("codigo").update({"partes_corretas": ""})
            else:
                db.child("codigo").update({"num_tentativas": n_tentativas+1})
                db.child("codigo").update({"partes_corretas": ""})
