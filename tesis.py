#!/usr/bin/python
# -*- coding: utf-8 -*-
#librerias y bibliotecas importadas
from py532lib.i2c import *
from py532lib.frame import *
from py532lib.constants import *
import csv
import mysql.connector
import time
#Constantes definidas
pathCodigoRFID = "codigosRFID.csv"
pathTempTransaccion = "TempTransaccion.csv"
pathModoSistema = "modoSistema.csv"

pn532 = Pn532_i2c()
pn532.SAMconfigure()

#LEE EL CODIGO ESCANEADO
def leeCodigoRFID(): 
    codigoRFID = pn532.read_mifare().get_data()
    return codigoRFID
# Se evalua se el sistema esta HABILITADO o NO (estado.txt 1=HABILITADO, 0= DESHABILITADO)
def inicioSistema():  
    fileWriter = open(pathModoSistema, 'w')
    writer = csv.writer(fileWriter)
    # Posicion 0 es modo y posicion 1 es estado
    writer.writerow([int('1'), int('1')])  
    fileWriter.close()

# Se evalua el modo del sistema, esta En modo Caja(1=Modo Caja, 0=Modo Chequeo Precio)
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

inicioSistema()
print("Sistema de Caja")

while estadoSistema()== 1:
    fileWriter = open(pathCodigoRFID, 'w')
    fileWriter.close()
    #Modo de hacer lista de articulos
    while modoSistema()==1: 
        bandera=0
        codigoRFID=leeCodigoRFID() 
        fileReader = open(pathCodigoRFID, 'r')
        reader = csv.reader(fileReader)
        for fila in reader:
            dato = fila[0]
            if str(dato) == str(codigoRFID):
                bandera=1             
        fileReader.close()
        if bandera == 0:
            fileWriter = open(pathCodigoRFID, 'a')
            writer = csv.writer(fileWriter)
            writer.writerow([str(codigoRFID)])
            fileWriter.close()
            print("Articulo: ",codigoRFID)   
        else:
            print("No se encontro")

    #Modo de agregar Articulo y Modo de chequeo Precio
    while modoSistema() == 2:   
        time.sleep(1)
        print("Sistema de chequeo y agregar codigo")
        codigoRFID1=leeCodigoRFID()
        codigoRFID2=leeCodigoRFID()
        if str(codigoRFID1) == str(codigoRFID2):
            print("Agrego codigo")
            fileWriter = open(pathCodigoRFID, 'w')
            writer = csv.writer(fileWriter)
            writer.writerow([str(codigoRFID1)])
            fileWriter.close()
        else:
            print("Error al agregar codigo")
            fileWriter = open(pathCodigoRFID, 'w')
            writer = csv.writer(fileWriter)
            writer.writerow([str("ErrorCodigo")])
            fileWriter.close()