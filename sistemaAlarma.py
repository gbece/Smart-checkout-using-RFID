#!/usr/bin/python
# -*- coding: utf-8 -*-
#librerias y bibliotecas importadas
from py532lib.i2c import *
from py532lib.frame import *
from py532lib.constants import *
import csv
from pathlib import Path
import mysql.connector
import time
from mysql.connector import Error
import RPi.GPIO as GPIO
import threading
#Constantes definidas
pathCodigoRFIDAlarma = "logCodigosRFIDAlarma.csv"
pathTempTransaccion = "TempTransaccion.csv"
pathEstadoSistema = "estado.txt"
pathModoSistema = "modoSistema.csv"
#Definicion de base de datos
baseDatos = mysql.connector.connect(host="localhost",
                                    user="admin",
                                    password="raspberry",
                                    database="Datos",
                                    port="3306"
)

GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.OUT)
miCursor = baseDatos.cursor()

pn532 = Pn532_i2c()
pn532.SAMconfigure()
#LEE EL CODIGO ESCANEADO
def leeCodigoRFID(): 
    codigoRFID = pn532.read_mifare().get_data()
    return codigoRFID

def existeArticulo(codigoRFID):
    bandera = False
    sql = "SELECT * FROM Tags WHERE Codigo = %s"
    miCursor.execute(sql, (str(codigoRFID),))
    myresult = miCursor.fetchall()
    if myresult != []:
        bandera = True
    return bandera

def sePagoArticulo(codigoRFID):
    bandera = False
    sql = "SELECT * FROM Tags WHERE Codigo = %s"
    miCursor.execute(sql, (str(codigoRFID),))
    myresult = miCursor.fetchall()
    if myresult != []:
        lista = list (myresult[0])
        sePagoBuscado = int(lista[5])
        if sePagoBuscado == 1:
            bandera = True
    return bandera

#BUSCA EL ARTICULO POR CODIGO
def getArticulo(codigoRFID): 
        sql = "SELECT * FROM Tags WHERE Codigo = %s"
        miCursor.execute(sql, (str(codigoRFID),))
        myresult = miCursor.fetchall()
        if myresult != []:
            lista = list (myresult[0])
            idBuscado = lista[0]
            descripcionBuscada = lista[2]
            precioBuscado = lista[3]
            pagoBuscado = lista[4]
        ##Devuelve una lista con los datos del articulo
        return lista  

#AGREGA EL ARTICULO AL ARCHIVO DE STOCK.
def agregaArticulo(unCodigo, unCodigoProducto, unaDescripcion, unPrecio, unPago): 
    sql = "INSERT INTO Tags (Codigo, CodigoProducto, Descripcion, Precio, Pago) VALUES (%s,%s,%s,%s,%s)"
    val = (str(unCodigo), int(unCodigoProducto),str(unaDescripcion), int(unPrecio), int(unPago))
    miCursor.execute(sql,val)
    baseDatos.commit()

#RESETEA EL ARCHIVO TempTransaccion.csv
def resetCodME(): 
    fileWriter = open(pathCodME, 'w')
    writer = csv.writer(fileWriter)
    writer.writerow(["0","Escanee producto"])
    fileWriter.close()
    
# Se evalua se el sistema esta HABILITADO o NO (estado.txt 1=HABILITADO, 0= DESHABILITADO)
def estadoSistema():  
    bandera = False
    fileReader = open(pathEstadoSistema, 'r')
    if fileReader.read(1) == '0':
        bandera = False
    else:
    	bandera = True
    fileReader.close()
    return bandera
    
# Se evalua se el sistema esta HABILITADO o NO (estado.txt 1=HABILITADO, 0= DESHABILITADO)
def inicioSistema():  
    fileWriter = open(pathModoSistema, 'w')
    writer = csv.writer(fileWriter)
    # Posicion 0 es modo y posicion 1 es estado
    writer.writerow([int('1'), int('1')])  
    fileWriter.close()
    print("Bienvenido al Sistema de Alarma")
    if not(Path(pathCodigoRFIDAlarma).exists()):
        fileWriter = open(pathCodigoRFIDAlarma, 'w')
        writer = csv.writer(fileWriter)
        writer.writerow(["Descripcion", "Codigo de Articulo", "Precio Articulo", "Esta pago", "Codigo RFID"])
        fileWriter.close()
    
def modoSistema():  
    fileReader = open(pathModoSistema, 'r')
    reader = csv.reader(fileReader)
    fila = next(reader)
    modo=int(fila[0])
    fileReader.close()
    return modo

# Se evalua se el sistema esta HABILITADO o NO (1=HABILITADO, 0= DESHABILITADO)
def estadoSistema():  
    fileReader = open(pathModoSistema, 'r')
    reader = csv.reader(fileReader)
    fila = next(reader)
    estado=int(fila[1])
    fileReader.close()
    return estado

def apagarAlarma():
    GPIO.output(16,GPIO.LOW)

inicioSistema()

while estadoSistema()==1:
    while modoSistema()==1:
        bandera=0
        codigoRFID=leeCodigoRFID()
        if existeArticulo(codigoRFID) and not(sePagoArticulo(codigoRFID)):
            GPIO.output(16,GPIO.HIGH)
            t = threading.Timer(3.0, apagarAlarma)
            t.start()
            articulo = getArticulo(codigoRFID)
            codigoArticuloBuscado= articulo[2]
            descripcionBuscada = articulo[3]
            precioBuscado=articulo[4]
            sePagoBuscado=articulo[5]
            fileReader = open(pathCodigoRFIDAlarma, 'r')
            reader = csv.reader(fileReader)
            for fila in reader:
                dato = fila[4]
                if str(dato) == str(codigoRFID):
                    bandera=1           
            fileReader.close()
            if bandera == 0:
                fileWriter = open(pathCodigoRFIDAlarma, 'a')
                writer = csv.writer(fileWriter)
                writer.writerow([str(descripcionBuscada), int(codigoArticuloBuscado), int(precioBuscado),str("No"), str(codigoRFID)])
                fileWriter.close()
                print("Se detecto que el articulo", str(descripcionBuscada),"con el codigo de articulo ", int(codigoArticuloBuscado)," y el precio", int(precioBuscado) ," no se pago")
            
if (baseDatos.is_connected()):
        cursor.close()
        baseDatos.close()