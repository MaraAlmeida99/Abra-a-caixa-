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
    #output = b'JOYSTICK LUR\r\n'
    #output1 = b'TOUCHPAD SSSSS\r\n'
    print(output)
    print(output1)
    
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
        #n_tentativas = 0
        print(partes_corretas)
        print(n_tentativas)
        if tipo == b"KEYPAD":
            codigo_db = db.child("chave").child("codigo_numerico").get().val()
            #codigo_db = "4444" #b"4444"
            print( codigo_db )
            print( type(codigo_db) )
            print (cod.decode('utf-8'))
            print ( type(cod.decode('utf-8')) )
            if cod.decode('utf-8') == codigo_db:
                ordem_db = db.child("chave").child("codigo_ordem").get().val()
                #ordem_db = "312"
                print("passa")
                print( ordem_db[1] )
                print ( ord_cod_num )
                if ordem_db[0] == ord_cod_num:
                    db.child("codigo").update({"partes_corretas": ord_cod_num})
                    #partes_corretas = ord_cod_num
                elif ordem_db[1] == ord_cod_num:
                    print ( "Debug0")
                    print ( partes_corretas )
                    print ( len(partes_corretas) )
                    if len(partes_corretas) == 1:
                        db.child("codigo").update({"partes_corretas": partes_corretas+ord_cod_num})
                        #partes_corretas += ord_cod_num
                    else:
                        print("aqui")
                        db.child("codigo").update({"num_tentativas": n_tentativas+1})
                        db.child("codigo").update({"partes_corretas": ""})
                    	#n_tentativas += 1 
                elif ordem_db[2] == ord_cod_num:
                    if len(partes_corretas) == 2:
                        db.child("codigo").update({"partes_corretas": partes_corretas+ord_cod_num})
                        db.update({"estado": "Aberto"})
                        db.child("codigo").update({"partes_corretas": ""})
                        #partes_corretas += ord_cod_num
                        #estado = "Aberto"
                    else:
                        db.child("codigo").update({"num_tentativas": n_tentativas+1})
                        db.child("codigo").update({"partes_corretas": ""})
                        #n_tentativas += 1
                else:
                    db.child("codigo").update({"num_tentativas": n_tentativas+1})
                    db.child("codigo").update({"partes_corretas": ""})
                    #num_tentativas += 1
            else:
                db.child("codigo").update({"num_tentativas": n_tentativas+1})
                db.child("codigo").update({"partes_corretas": ""})
                n_tentativas += 1
                partes_corretas = ""

        elif tipo == b"JOYSTICK":
            print("Debug 0")
            codigo_db = db.child("chave").child("codigo_rotacoes").get().val()
            #codigo_db = "LUR"
            print(codigo_db)
            if cod.decode('utf-8') == codigo_db:
                print("DEbug1")
                ordem_db = db.child("chave").child("codigo_ordem").get().val()
                #ordem_db = "312"
                if ordem_db[0] == ord_cod_rot:
                    print("DEBUG2")
                    db.child("codigo").update({"partes_corretas": ord_cod_rot})
                    #partes_corretas = ord_cod_rot
                elif ordem_db[1] == ord_cod_rot:
                    if len(partes_corretas) == 1:
                        db.child("codigo").update({"partes_corretas": partes_corretas+ord_cod_rot})
                        #partes_corretas += ord_cod_rot
                    else:
                        db.child("codigo").update({"num_tentativas": n_tentativas+1})
                        db.child("codigo").update({"partes_corretas": ""})
                        #n_tentativas += 1
                elif ordem_db[2] == ord_cod_rot:
                    if len(partes_corretas) == 2:
                        db.child("codigo").update({"partes_corretas": partes_corretas+ord_cod_rot})
                        db.update({"estado": "Aberto"})
                        db.child("codigo").update({"partes_corretas": ""})
                        #partes_corretas += ord_cod_rot
                        #estado = "Aberto"
                    else:
                        db.child("codigo").update({"num_tentativas": n_tentativas+1})
                        db.child("codigo").update({"partes_corretas": ""})
                        #n_tentativas += 1
                else:
                    db.child("codigo").update({"num_tentativas": n_tentativas+1})
                    db.child("codigo").update({"partes_corretas": ""})
                    #n_tentativas += 1
            else:
                db.child("codigo").update({"num_tentativas": n_tentativas+1})
                db.child("codigo").update({"partes_corretas": ""})
                #n_tentativas += 1
                #partes_corretas = ""
        else:
            codigo_db = db.child("chave").child("codigo_batidas").get().val()
            #codigo_db = "SSSSS" #b"SSSSS"

            if cod.decode('utf-8') == codigo_db:
                ordem_db = db.child("chave").child("codigo_ordem").get().val()
                #ordem_db = "312"
                print ( ordem_db )
                print (ordem_db[2])
                print ( ord_cod_bat )
                if ordem_db[0] == ord_cod_bat:
                    db.child("codigo").update({"partes_corretas": ord_cod_bat})
                    #partes_corretas += ord_cod_bat
                elif ordem_db[1] == ord_cod_bat:
                    if len(partes_corretas) == 1:
                        db.child("codigo").update({"partes_corretas": partes_corretas+ord_cod_bat})
                        #partes_corretas += ord_cod_bat
                    else:
                        db.child("codigo").update({"num_tentativas": n_tentativas+1})
                        db.child("codigo").update({"partes_corretas": ""})
                        #n_tentativas += 1
                elif ordem_db[2] == ord_cod_bat:
                    if len(partes_corretas) == 2:
                        db.child("codigo").update({"partes_corretas": partes_corretas+ord_cod_bat})
                        db.update({"estado": "Aberto"})
                        db.child("codigo").update({"partes_corretas": ""})
                        #partes_corretas += ord_cod_bat
                        #estado += "Aberto"
                    else:
                        db.child("codigo").update({"num_tentativas": n_tentativas+1})
                        db.child("codigo").update({"partes_corretas": ""})
                        #n_tentativas += 1
                else:
                    db.child("codigo").update({"num_tentativas": n_tentativas+1})
                    db.child("codigo").update({"partes_corretas": ""})
                    #n_tentativas += 1
            else:
                db.child("codigo").update({"num_tentativas": n_tentativas+1})
                db.child("codigo").update({"partes_corretas": ""})
                #n_tentativas += 1
                #partes_corretas = ""

    print("-------------------")
    print("partes_corretas: " + partes_corretas)
    print("n_tentativas: "+ str(n_tentativas))
    print("estado: "+ estado)
