#!/usr/bin/python

#librerias y bibliotecas importadas
from tkinter import *
import tkinter as tk
from tkinter import font
import csv
import Datos
import constantes
import time

#Indica el modo al sistema de escaneo
def cambiarModo():
    fileWriter = open(constantes.ESTADO, 'w')
    writer = csv.writer(fileWriter)
    writer.writerow([int('2')])
    fileWriter.close()

#Obtener precio del producto escaneado desde la base de datos
def devuelvePrecio():
    global precio
    precio = None
    global producto
    producto = None
    contLineas = 0
    with open(constantes.ARCHIVO) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='@')
        for row in csv_reader:
            if (row[0] == "ErrorCodigo"):
                etiquetaPrecio['text'] = 'Vuelva a escanear el articulo' 
                root.after(5000, limpiarArchivo)
            else:
                precio = db.devolverPrecio(row[0])
                producto  = db.devolverProducto(row[0])
                contLineas = 1

    if contLineas == 1:
       mostrarPrecio()
    else:  
       root.after(1000, devuelvePrecio)  

#Se muestra descripcion y precio del producto escaneado en caso de existir
def mostrarPrecio():
    if (producto == []):
        etiquetaPrecio['text'] = 'Precio no disponible' 
    else:
        etiqueta['text'] = producto[0][1]
        etiquetaPrecio['text'] = 'El precio es: $' + str(precio[0][0])
    root.after(5000, limpiarArchivo)

#Se borra el codigo del archivo
def limpiarArchivo():
    etiqueta['text'] = 'Escanee el producto'
    etiquetaPrecio['text'] = ''
    fileWriter = open(constantes.ARCHIVO,'w')
    fileWriter.close()
    root.after(1000, devuelvePrecio)

#Inicio del programa
#Se crea la ventana de la estacion de consulta de precio
db = Datos.datos()
global archivo
global auxPrecio
root = tk.Tk()
root.attributes('-zoomed',True)
root.title("Consulta de Precio")
fuenteConsultaPrecio = font.Font(family="Helvetica",size=36,weight="bold")
etiqueta = tk.Label(root, text="", 
                        font=fuenteConsultaPrecio)
etiqueta['text'] = 'Escanee el producto'
etiqueta.pack(side = TOP,padx = 100 , pady = 100)
etiquetaPrecio = tk.Label(root, text="", 
                        font=fuenteConsultaPrecio)
etiquetaPrecio.pack(side = TOP,padx = 100 , pady = 100)
cambiarModo()
devuelvePrecio()
root.mainloop()