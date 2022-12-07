#!/usr/bin/python

#librerias y bibliotecas importadas
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import font
import csv
import Datos
import constantes
from array import *
import time

#Indica el modo al sistema de escaneo
def cambiarModo():
    fileWriter = open(constantes.ESTADO, 'w')
    writer = csv.writer(fileWriter)
    writer.writerow([int('1')])
    fileWriter.close()

#Se elimina artciculo de la caja
def eliminarArticulo():
    global lista
    try:
        for row in lista:
            if (tabla.item(tabla.selection())['values'][0] == row[0][1]):
                lista.remove(row)
                id =row[0][0]
                borrar(id)
                limpiar()
        leerArchivo()
    except IndexError as e:
        mensaje['text'] = 'Seleccione un artiulo'
        return

#Se borra codigo del archivo correspondiente al articulo a eliminar
def borrar(id):
    f = open(constantes.ARCHIVO, "r")
    lineas = f.readlines()
    f.close()
    lineaBorrar = db.devolverCodigo(id)
    f = open(constantes.ARCHIVO, "w")
    lineaAux = str(lineaBorrar[0][0]) + "\n"
    for linea in lineas:
        if linea != lineaAux:
            f.write(linea)
    f.close()

#Para escanear productos que por error no fueron escaneados
def faltanArticulos():
    global controlArticulos
    controlArticulos = 1
    mensaje['text'] = 'Saque los articulos que aparecen en pantalla de la bandeja'
    leerArchivo()

#Verifica si hay productos para pagar
def realizarPago():
    global total
    if (total == 0):
        mensaje['text'] = 'No hay productos para pagar'
    else:
        pagar()

#Se gestiona el pago de los productos
def pagar():
    global total
    pago = Toplevel()
    pago.title("Pagar")
    pago.attributes('-zoomed',True)
    fuentePago = font.Font(family="Helvetica",size=36,weight="bold")
    strTotal = str(total)
    etiquetaPago = tk.Label(pago, text= "El total a pagar es $"+ strTotal, 
                            font=fuentePago)
    etiquetaPago.pack(side = TOP,padx = 200, pady = 100)
    def aceptaPago():
        global lista
        for row in lista:
            db.realizarPago(row[0][0])
        limpiar()
        limpiarArchivo()
        print("Lista ", lista)
        pago.destroy()
        leerArchivo()
    botonPago = tk.Button(pago, text = "Aceptar",command = aceptaPago ,font=fuentePago)
    botonPago.pack(side = BOTTOM, ipady = 100, ipadx = 200, pady = 100)

#Limpia el archivo y la tabla de la caja cuando se cancela compra
def cancelarCompra():
    limpiar()
    limpiarArchivo()

#Borra todos los codigos del archivo
def limpiarArchivo():
    fileWriter = open(constantes.ARCHIVO,'w')
    fileWriter.close()
    leerArchivo()

#Borra todos los articulos de la tabla de la caja
def limpiar():
    for i in tabla.get_children():
       tabla.delete(i)
    global listaAux, lista, total
    total = 0
    listaAux = []
    lista = []

#Lectura del archivo donde estan los codigos de los productos escaneados
def leerArchivo():
    global controlArticulos, lista
    hayArticuloNuevo = 0
    with open(constantes.ARCHIVO) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='@')
        for row in csv_reader:
            esta = 0
            articulo = db.devolverProducto(row[0])
            print(articulo)
            if (articulo != []):
                if (articulo[0][3] == 1):
                    mensaje['text'] = 'El articulo ya fue pago'
                else:
                    mensaje['text'] = ''
                    for x in range(len(lista)):
                        if (lista[x] == articulo):
                            esta = 1
                    if (esta == 0):
                        hayArticuloNuevo = 1
                        lista.append(articulo)
    if (lista != [] and hayArticuloNuevo):
        listarProductosCaja()
    else:
        caja.after(1000, leerArchivo)

#Agrega los productos escaneados a la tabla de la caja
def listarProductosCaja():
    global total, lista, listaAux, controlArticulos
    index = iid = 0
    for row in lista:
        if row != None:
            if (not(row in listaAux)):
                tabla.insert("", index, text = iid, values=(row[0][1],row[0][2]))
                listaAux.append(row)
                total += row[0][2]
            else:
                print("ERROR")
        index = iid = index + 1
    caja.after(1000,leerArchivo)

#Inicio del programa
#Se crea la tabla de la caja sin productos  
db = Datos.datos()
global lista
caja = tk.Tk()
caja.attributes('-zoomed',True)
caja.title("Caja")
fuenteCaja = font.Font(family="Helvetica",size=24,weight="bold")
tabla = ttk.Treeview( caja, height=10, columns=('Descripcion', 'Precio'), selectmode="extended")
tabla.heading('#0', text='ID', anchor=tk.CENTER)
tabla.heading('#1', text='Descripcion', anchor=tk.CENTER)
tabla.heading('#2', text='Precio', anchor=tk.CENTER)
tabla.column('#1', stretch=tk.YES, minwidth=50, width=800)
tabla.column('#2', stretch=tk.YES, minwidth=50, width=200)
tabla.column('#0', stretch=tk.YES, minwidth=50, width=60)
tabla.grid(row=2, column=2, columnspan=4,padx=100,pady=50)
fuenteMensaje = font.Font(size=16)
mensaje= Label(caja, text='',fg = 'red',font=fuenteMensaje)
mensaje.grid(row = 3, column = 2, columnspan = 3, sticky = W + E)
botonSobranArticulos = tk.Button(caja, text = "Eliminar Articulo",command = eliminarArticulo, font=fuenteCaja)
botonSobranArticulos.grid(row = 4, column = 2, ipadx = 75, ipady = 30,padx=100,pady=30)
botonFaltanArticulos = tk.Button(caja, text = "Faltan Articulos",command = faltanArticulos, font=fuenteCaja)
botonFaltanArticulos.grid(row = 4, column = 4, ipadx = 75, ipady = 30,padx=100,pady=30)
botonPagar = tk.Button(caja, text = "Pagar",command = realizarPago, font=fuenteCaja)
botonPagar.grid(row = 6, column = 2,  ipadx = 160, ipady = 30,padx=30,pady=10)
botonCancelarCompra = tk.Button(caja, text = "Cancelar",command = cancelarCompra, font=fuenteCaja)
botonCancelarCompra.grid(row = 6, column = 4,  ipadx = 130, ipady = 30,padx=30,pady=10)
cambiarModo()
limpiar()
limpiarArchivo()
mainloop()