#!/usr/bin/python

#librerias y bibliotecas importadas
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import font
import getpass
import csv
import Datos
import constantes
from array import *
import time
import hashlib


class Aplicacion():
    #Inicio de programa
    def __init__(self):
        global auxPrecio
        auxPrecio = 0
        global controlConsulta
        controlConsulta = 0
        global usuarioActivo
        self.db = Datos.datos()
        self.ventana = tk.Tk()
        self.ventana.attributes('-zoomed',True)
        self.ventana.resizable(0,0)
        self.ventana.title("Menu")
        self.botonRegistrarProducto = tk.Button(self.ventana, text = "Registrar Producto", command = self.registrarProducto, activebackgroun = "red")
        self.botonRegistrarProducto.place(rely = 0.255, relwidth= 1, relheight = 0.09)
        self.botonRegistrarUsuario = tk.Button(self.ventana, text = "Registrar Usuario", command = self.registroUsuario,activebackgroun = "red")
        self.botonRegistrarUsuario.place(rely = 0.355, relwidth = 1, relheight = 0.09)
        self.botonBajaUsuario = tk.Button(self.ventana, text = "Baja de Usuario",  command = self.bajaUsuario ,activebackgroun = "red")
        self.botonBajaUsuario.place(rely = 0.455, relwidth = 1, relheight = 0.09)
        self.botonBuscarProducto = tk.Button(self.ventana, text = "Buscar por Producto", command = self.buscarProducto,  activebackgroun = "red")
        self.botonBuscarProducto.place(rely = 0.555, relwidth = 1, relheight = 0.09)
        self.botonSalir = tk.Button(self.ventana, text = "Salir", command = self.ventana.destroy,  activebackgroun = "red")
        self.botonSalir.place(rely = 0.655, relwidth = 1, relheight = 0.09)
        self.IniciarSesion()
        self.ventana.mainloop()

    #Ventana de inicio de sesion
    def IniciarSesion(self):
        self.inicioSesion = Toplevel()
        self.inicioSesion.title("Iniciar Sesion")
        self.inicioSesion.geometry("430x200")
        self.inicioSesion.resizable(0,0)
        self.fuente = font.Font(weight='bold')                       
        self.etiq1 = ttk.Label(self.inicioSesion, text="Usuario:", 
                               font=self.fuente)
        self.etiq2 = ttk.Label(self.inicioSesion, text="Contraseña:", 
                               font=self.fuente) 
        self.mensa = StringVar()
        self.etiq3 = ttk.Label(self.inicioSesion, textvariable=self.mensa, 
                     font=self.fuente, foreground='blue')         
        self.usuario = StringVar()
        self.clave = StringVar()
        self.usuario.set(getpass.getuser())
        self.ctext1 = ttk.Entry(self.inicioSesion, textvariable=self.usuario,width=30)
        self.ctext1.delete(0, tk.END)
        self.ctext2 = ttk.Entry(self.inicioSesion, textvariable=self.clave, 
                                width=30, show="*")
        self.separ1 = ttk.Separator(self.inicioSesion, orient=HORIZONTAL)
        self.boton1 = ttk.Button(self.inicioSesion, text="Aceptar", 
                                 padding=(5,5), command=self.aceptar)
        self.boton2 = ttk.Button(self.inicioSesion, text="Cancelar", 
                                 padding=(5,5), command=self.ventana.destroy)      
        self.etiq1.place(x=30, y=40)
        self.etiq2.place(x=30, y=80)
        self.etiq3.place(x=150, y=120)
        self.ctext1.place(x=150, y=42)
        self.ctext2.place(x=150, y=82)
        self.separ1.place(x=5, y=145, bordermode=OUTSIDE, 
                          height=10, width=420)
        self.boton1.place(x=170, y=160)
        self.boton2.place(x=290, y=160)
        self.ctext1.focus_set()
        self.inicioSesion.transient(master=self.ventana)
        self.inicioSesion.grab_set()
        self.ventana.wait_window(self.inicioSesion)

    #Verificar usuario y contraseña correctos
    def aceptar(self):
        aux = self.usuario.get()
        clave = self.db.consultaClave(aux)
        if self.clave.get() == clave[0][0]:
            self.etiq3.configure(foreground='blue')
            self.inicioSesion.destroy()           
        else:
            self.etiq3.configure(foreground='red')
            self.mensa.set("Clave incorrecta")

    #Ventana registrar productos
    def registrarProducto(self):
        self.registroProducto = Toplevel(self.ventana)
        self.registroProducto.geometry("530x320")
        self.registroProducto.resizable(0,0)
        self.registroProducto.title("Resgistrar Producto")
        global controlRegistro
        controlRegistro = 0
        self.fuenteRegistroPaquete = font.Font(weight='bold')   
        self.etiquetaEscanear = ttk.Label(self.registroProducto, text = "Pase la etiqueta del producto por el lector e ingrese\nlos datos del producto",
                                font=self.fuenteRegistroPaquete)                    
        self.etiquetaDescripcion = ttk.Label(self.registroProducto, text="Descripcion:", 
                               font=self.fuenteRegistroPaquete)
        self.etiquetaCodigoProducto = ttk.Label(self.registroProducto, text="Codigo del producto:", 
                               font=self.fuenteRegistroPaquete)
        self.etiquetaPrecio = ttk.Label(self.registroProducto, text="Precio:", 
                               font=self.fuenteRegistroPaquete)
        self.mensaje = StringVar()
        self.etiquetas = ttk.Label(self.registroProducto, textvariable=self.mensaje, 
                     font=self.fuenteRegistroPaquete, foreground='blue')          
        self.descripcion = StringVar()
        self.codigoProducto = StringVar()
        self.precioProducto = StringVar()
        self.ctextDescripcion = ttk.Entry(self.registroProducto, textvariable=self.descripcion,width=30)
        self.ctextDescripcion.delete(0, tk.END)
        self.ctextCodigoProducto = ttk.Entry(self.registroProducto, textvariable=self.codigoProducto, 
                                width=30)
        self.ctextPrecio = ttk.Entry(self.registroProducto, textvariable=self.precioProducto,width=30)
        self.mensajeRegistroProd = Label(self.registroProducto, text = '', fg = 'red' )
        self.separ = ttk.Separator(self.registroProducto, orient=HORIZONTAL)
        self.botonAceptarProducto = ttk.Button(self.registroProducto, text="Aceptar", 
                                 padding=(5,5), command=self.escanearTag)
        self.botonCancelarProducto = ttk.Button(self.registroProducto, text="Cancelar", 
                                 padding=(5,5), command=self.registroProducto.destroy)
        self.etiquetaEscanear.place(x=30, y=20)          
        self.etiquetaDescripcion.place(x=30, y=80)
        self.etiquetaCodigoProducto.place(x=30, y=120)
        self.etiquetaPrecio.place(x=30, y=160)
        self.etiquetas.place(x=300, y=1600)
        self.ctextDescripcion.place(x=250, y=82)
        self.ctextCodigoProducto.place(x=250, y=122)
        self.ctextPrecio.place(x=250, y=162)
        self.mensajeRegistroProd.place(x=110, y=205)
        self.separ.place(x=5, y=245, bordermode=OUTSIDE, 
                          height=10, width=520)
        self.botonAceptarProducto.place(x=170, y=270)
        self.botonCancelarProducto.place(x=290, y=270)
        self.ctextDescripcion.focus_set()
        self.registroProducto.transient(master=self.ventana)
        self.registroProducto.grab_set()
        self.ventana.wait_window(self.registroProducto)

    #Funcion para ecanear tag para registrar producto
    def escanearTag(self):
        global codigo, controlRegistro
        if (controlRegistro == 0):
            with open(constantes.ARCHIVO) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter='@')
                for row in csv_reader:
                    if (row[0] == "ErrorCodigo"):
                        self.mensajeRegistroProd['text'] = 'Error al escanear articulo, intente nuevamente' 
                        self.limpiarArchivo()
                    else:
                        if (not(self.db.existeArticulo(row[0]))):
                            self.mensajeRegistroProd['text'] = ''
                            codigo = row[0]
                            self.limpiarArchivo()
                            self.agregarProducto()
                        else:
                            self.mensajeRegistroProd['text'] = 'Etiqueta asignada a otro articulo, intente nuevamente'  
                            self.limpiarArchivo()     
        else:
            self.agregarProducto()

    #Ventana para agregar nuevo producto
    def agregarProducto(self):
        global codigo, controlRegistro
        maxId = self.db.devolverMaxIdTags()
        if (self.descripcion.get() == ""):
            self.mensajeRegistroProd['text'] = 'Faltan ingresar la descripcion'
            controlRegistro = 1
        elif(self.codigoProducto.get() == ""):
            self.mensajeRegistroProd['text'] = 'Falta ingresar el codigo'
            controlRegistro = 1
        elif(self.precioProducto.get() == ""):
            self.mensajeRegistroProd['text'] = 'Faltan ingresar el precio'
            controlRegistro = 1
        else:    
            self.mensajeRegistroProd['text'] = ''
            dato = (maxId[0][0] + 1,codigo, self.codigoProducto.get(), self.descripcion.get(), self.precioProducto.get())
            self.db.altaProducto(dato)
            codigo = ""
            self.descripcion.set("")
            self.codigoProducto.set("")
            self.precioProducto.set("")
            controlRegistro = 0
            self.registroProducto.destroy()

    #Ventana para registrar nuevo usuario
    def registroUsuario(self):
        self.agregarUsuario = Toplevel(self.ventana)
        self.agregarUsuario.title("Registar Usuario")
        self.agregarUsuario.geometry("430x200")
        self.agregarUsuario.resizable(0,0)
        self.fuente = font.Font(weight='bold')                       
        self.etiq1 = ttk.Label(self.agregarUsuario, text="Usuario:", 
                               font=self.fuente)
        self.etiq2 = ttk.Label(self.agregarUsuario, text="Contraseña:", 
                               font=self.fuente)     
        self.mensa = StringVar()
        self.etiq3 = ttk.Label(self.agregarUsuario, textvariable=self.mensa, 
                     font=self.fuente, foreground='blue')
        self.usuario = StringVar()
        self.clave = StringVar()
        self.usuario.set(getpass.getuser())
        self.ctext1 = ttk.Entry(self.agregarUsuario,  textvariable=self.usuario ,width=30)
        self.ctext1.delete(0, tk.END)
        self.ctext2 = ttk.Entry(self.agregarUsuario, textvariable=self.clave, 
                                width=30, show="*")
        self.separ1 = ttk.Separator(self.agregarUsuario, orient=HORIZONTAL)
        self.boton1 = ttk.Button(self.agregarUsuario, text="Registrar", 
                                 padding=(5,5), command=self.agregar)
        self.boton2 = ttk.Button(self.agregarUsuario, text="Cancelar", 
                                 padding=(5,5), command=self.agregarUsuario.destroy)              
        self.etiq1.place(x=30, y=40)
        self.etiq2.place(x=30, y=80)
        self.etiq3.place(x=150, y=120)
        self.ctext1.place(x=150, y=42)
        self.ctext2.place(x=150, y=82)
        self.separ1.place(x=5, y=145, bordermode=OUTSIDE, 
                          height=10, width=420)
        self.boton1.place(x=170, y=160)
        self.boton2.place(x=290, y=160)
        self.ctext1.focus_set()
        self.agregarUsuario.transient(master=self.ventana)
        self.agregarUsuario.grab_set()
        self.ventana.wait_window(self.agregarUsuario)

    #Funcion para eliminar usuario
    def bajaUsuario(self):
        self.eliminarUsuario = Toplevel(self.ventana)
        self.eliminarUsuario.title("Eliminar Usuario")
        self.eliminarUsuario.geometry("430x200")
        self.eliminarUsuario.resizable(0,0)
        self.fuente = font.Font(weight='bold')                       
        self.etiquetaUsuarioBaja = ttk.Label(self.eliminarUsuario, text="Usuario:", 
                               font=self.fuente)
        self.mensa = StringVar()
        self.etiquetaMensaje = ttk.Label(self.eliminarUsuario, textvariable=self.mensa, 
                     font=self.fuente, foreground='blue')          
        self.usuarioBaja = StringVar()
        self.usuario.set(getpass.getuser())
        self.ctextUsuarioBaja = ttk.Entry(self.eliminarUsuario,  textvariable=self.usuarioBaja ,width=30)
        self.ctextUsuarioBaja.delete(0, tk.END)
        self.separBaja = ttk.Separator(self.eliminarUsuario, orient=HORIZONTAL)
        self.botonAceptarBaja = ttk.Button(self.eliminarUsuario, text="Aceptar", 
                                 padding=(5,5), command=self.baja)
        self.botonCancelarBaja = ttk.Button(self.eliminarUsuario, text="Cancelar", 
                                 padding=(5,5), command=self.eliminarUsuario.destroy)                                  
        self.etiquetaUsuarioBaja.place(x=30, y=40)
        self.etiquetaMensaje.place(x=150, y=120)
        self.ctextUsuarioBaja.place(x=150, y=42)
        self.separBaja.place(x=5, y=145, bordermode=OUTSIDE, 
                          height=10, width=420)
        self.botonAceptarBaja.place(x=170, y=160)
        self.botonCancelarBaja.place(x=290, y=160)
        self.ctextUsuarioBaja.focus_set()
        self.eliminarUsuario.transient(master=self.ventana)
        self.eliminarUsuario.grab_set()
        self.ventana.wait_window(self.eliminarUsuario)

    #Ventana para buscar productos
    def buscarProducto(self):
        self.busquedaProducto = Toplevel()
        self.busquedaProducto.title("Buscar producto")
        self.fuenteBusqueda = font.Font(weight='bold')
        self.frameBusqueda = LabelFrame(self.busquedaProducto, text = 'Buscar productos', font=self.fuenteBusqueda)
        self.etiquetaBusqueda = ttk.Label(self.frameBusqueda, text="Descripcion:")
        self.descripcionBusqueda = StringVar()
        self.ctextBusqueda = ttk.Entry(self.frameBusqueda, textvariable=self.descripcionBusqueda,width=30)
        self.ctextBusqueda.delete(0, tk.END)
        self.ctextBusqueda.focus()
        self.botonBusqueda = ttk.Button(self.frameBusqueda, text="Buscar", 
                                 padding=(5,5), command=self.cargoLista)
        self.mensajeBusqueda = Label(self.busquedaProducto, text = '', fg = 'red')
        self.tabla = ttk.Treeview(self.busquedaProducto, height = 15, columns = ('Descripcion', 'Precio','Pago'), selectmode="extended")
        self.botonBorrar = Button(self.busquedaProducto, text = 'Eliminar', command = self.borrarProducto)
        self.botonEditar = Button(self.busquedaProducto, text = 'Editar precio', command = self.editarProducto)
        self.frameBusqueda.grid(row = 0, column = 0, columnspan = 3, pady = 20) 
        self.etiquetaBusqueda.grid(row = 1 , column = 0,pady = 5)
        self.ctextBusqueda.grid(row = 1 , column = 1,pady = 5)
        self.botonBusqueda.grid(row = 3 , columnspan = 2, sticky = W + E)
        self.mensajeBusqueda.grid(row = 3, column = 0, columnspan = 2, sticky = W + E)
        self.tabla.grid(row = 4, column = 0, columnspan = 2)
        self.tabla.heading('#0', text = 'ID', anchor = tk.CENTER)
        self.tabla.heading('#1', text = 'Descripcion', anchor = tk.CENTER)
        self.tabla.heading('#2', text = 'Precio', anchor = tk.CENTER)
        self.tabla.heading('#3', text = 'Pago', anchor = tk.CENTER)
        self.tabla.column('#3', stretch=tk.YES, minwidth=50, width=80)
        self.tabla.column('#1', stretch=tk.YES, minwidth=50, width=200)
        self.tabla.column('#2', stretch=tk.YES, minwidth=50, width=100)
        self.tabla.column('#0', stretch=tk.YES, minwidth=50, width=50)
        self.botonBorrar.grid(row = 5, column = 0, sticky = W + E)
        self.botonEditar.grid(row = 5, column = 1, sticky = W + E)
        
    #Funcion para cargar datos de productos en lista
    def cargoLista(self):
        global productos
        productos = self.db.devolverProductos(self.descripcionBusqueda.get())
        self.mostrarProductos()

    #Funcion para mostrar productos en ventana buscarProductos
    def mostrarProductos(self):
        global productos
        index = 0
        iid = 1
        for i in self.tabla.get_children():
            self.tabla.delete(i)
        if (productos != []):
            for row in productos:
                self.mensajeBusqueda['text'] = ''
                self.tabla.insert("", index, text = iid, values=(row[1],row[2], row[3], row[0]))
                index += 1
                iid += 1
        else:
            self.mensajeBusqueda['text'] = 'No se encuentra producto'

    #Funcion para eliminar producto
    def borrarProducto(self):
        global productos
        try:
            self.mensajeBusqueda['text'] = ''  
            productoAux = self.tabla.item(self.tabla.selection())['values']
            self.db.bajaProducto(productoAux[3])
            for row in productos:
                if (productoAux[3] == row[0]):
                    productos.remove(row)
            self.mostrarProductos()
        except IndexError as e:
            self.mensajeBusqueda['text'] = 'Seleccione un artiulo'
            return

    #Funcion para editar producto
    def editarProducto(self):
        global productos
        productoAux = self.tabla.item(self.tabla.selection())['values']
        if (productoAux != ''):
            self.ventanaEditar()
            self.mensajeBusqueda['text'] = ''  
        else:
            self.mensajeBusqueda['text'] = 'Seleccione un artiulo'
            return
    
    #Ventana para editar precio
    def ventanaEditar(self):
        self.ventanaEdicion = Toplevel()
        self.ventanaEdicion.title("Editar producto")
        self.fuenteEdicion = font.Font(weight='bold')
        self.precio = IntVar()
        self.etiquetaPrecio = ttk.Label(self.ventanaEdicion, text="Nuevo precio:")
        self.ctextPrecio = ttk.Entry(self.ventanaEdicion, textvariable=self.precio,width=30)
        self.ctextPrecio.delete(0, tk.END)
        self.ctextPrecio.focus()
        self.botonPrecio = Button(self.ventanaEdicion, text='Aceptar', command=self.editarPrecio)
        self.etiquetaPrecio.grid(row = 1 , column = 0,pady = 5)
        self.ctextPrecio.grid(row = 1 , column = 1,pady = 5)
        self.botonPrecio.grid(row = 2, columnspan = 2, sticky = W + E)

    #Funcion para editar precio
    def editarPrecio(self):
        nuevoPrecio = self.precio.get()
        productoId = self.tabla.item(self.tabla.selection())['values'][3]
        dato = (nuevoPrecio, productoId)
        self.db.cambiarPrecio(dato)
        self.cargoLista()
        self.ventanaEdicion.destroy()

    #Funcion para agregar usuario
    def agregar(self):
        maxId = self.db.devolverMaxIdUsuarios()
        dato = (maxId[0][0] + 1, self.usuario.get(), self.clave.get())
        self.db.altaUsuario(dato)
        self.usuario.set("")
        self.clave.set("")
        self.agregarUsuario.destroy()

    #Funcion para baja de usuario
    def baja(self):
        dato = self.usuarioBaja.get()
        self.db.bajaUsuario(dato)
        self.usuarioBaja.set("")
        self.eliminarUsuario.destroy()

    #Funcion para eliminar codigos del archivo       
    def limpiarArchivo(self):
        fileWriter = open(constantes.ARCHIVO,'w')
        fileWriter.close()

#Funcion para indicar modo a sistema de escaneo
def cambiarModo():
    fileWriter = open(constantes.ESTADO, 'w')
    writer = csv.writer(fileWriter)
    writer.writerow([int('2')])
    fileWriter.close()

def main():
    cambiarModo()
    mi_app = Aplicacion()
    return(0)

if __name__ == '__main__':
    main()