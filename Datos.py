#Proceso donde se crean funciones para acceso a base de datos
#Se importa base de datos
import mysql.connector

class datos:
    #Se abre base de datos
    def abrir(self):
        conexion = mysql.connector.connect(host = "localhost",
                                                user = "root",
                                                password = "raspberry",
                                                database = "Datos")
        return conexion
    #Se crea usuario nuevo
    def altaUsuario(self, dato):
        conectar = self.abrir()
        cursor = conectar.cursor()
        sql = "INSERT INTO Usuarios(ID, Nombre, Clave) values (%s, %s, %s)"
        cursor.execute(sql, dato)
        conectar.commit()
        conectar.close()
    #Se elimina usuario
    def bajaUsuario(self, dato):
        conectar = self.abrir()
        cursor = conectar.cursor()
        sql = "DELETE FROM Usuarios WHERE Nombre=%s"
        cursor.execute(sql, (str(dato),))
        conectar.commit()
        conectar.close()
    #Consulta si existe usuario
    def consulta(self, dato):
        conectar = self.abrir()
        cursor = conectar.cursor()
        sql = "SELECT ID FROM Usuarios WHERE Nombre=%s"
        cursor.execute(sql, dato)
        resultado = cursor.fetchall() 
        conectar.close()
        return resultado
    #Consulta ultimo ID de usuraio para guardar siguiente usuario
    def devolverMaxIdUsuarios(self):
        conectar = self.abrir()
        cursor = conectar.cursor()
        sql = "SELECT Max(ID) FROM Usuarios"
        cursor.execute(sql)
        resultado = cursor.fetchall() 
        conectar.close()
        return resultado
    #Se consulta clave de usuario para inicio de sesion
    def consultaClave(self, dato):
        conectar = self.abrir()
        cursor = conectar.cursor()
        sql = "SELECT Clave FROM Usuarios WHERE Nombre=%s"
        cursor.execute(sql, (str(dato),))
        resultado = cursor.fetchall() 
        conectar.close()
        return resultado
    #Se agrega producto nuevo a la base de datos  
    def altaProducto(self, dato):
        conectar = self.abrir()
        cursor = conectar.cursor()
        sql = "INSERT INTO Tags(ID, Codigo, CodigoProducto, Descripcion, Precio) values (%s, %s, %s, %s, %s)"
        cursor.execute(sql, dato)
        conectar.commit()
        conectar.close()
    #Se elimina producto de la base de datos
    def bajaProducto(self, dato):
        conectar = self.abrir()
        cursor = conectar.cursor()
        sql = "DELETE FROM Tags WHERE ID=%s"
        cursor.execute(sql, (dato,))
        conectar.commit()
        conectar.close()
    #Se cambia la variable pago de producto que fue comprado
    def realizarPago(self,dato):
        conectar = self.abrir()
        cursor = conectar.cursor()
        sql = "UPDATE Tags SET Pago = 1 WHERE ID=%s"
        cursor.execute(sql, (dato,))
        conectar.commit()
        conectar.close()
    #Se edita precio de porducto solicitado
    def cambiarPrecio(self, dato):
        conectar = self.abrir()
        cursor = conectar.cursor()
        sql = "UPDATE Tags SET Precio=%s WHERE ID=%s"
        cursor.execute(sql, dato)
        conectar.commit()
        conectar.close()
    #Se consulta precio de producto solicitado
    def devolverPrecio(self, dato):
        conectar = self.abrir()
        cursor = conectar.cursor()
        sql = "SELECT Precio FROM Tags WHERE Codigo=%s"
        cursor.execute(sql, (str(dato),))
        resultado = cursor.fetchall()
        conectar.close()
        return resultado
    #Se consulta ID, descripcion, precio y si fue pago de producto solicitado
    def devolverProducto(self,dato):
        conectar = self.abrir()
        cursor = conectar.cursor()
        sql = "SELECT ID, Descripcion, Precio, Pago FROM Tags WHERE Codigo=%s"
        cursor.execute(sql, (str(dato),))
        resultado = cursor.fetchall() 
        conectar.close()
        return resultado
    #Se verifica si existe producto con sierto codigo
    def existeArticulo(self,dato):
        bandera = False
        conectar = self.abrir()
        cursor = conectar.cursor()
        sql = "SELECT * FROM Tags WHERE Codigo = %s"
        cursor.execute(sql, (str(dato),))
        resultado = cursor.fetchall()
        conectar.close()
        if resultado != []:
            bandera = True
        return bandera
    #Se verifica si producto solicitado fue pago
    def articuloPago(self,dato):
        conectar = self.abrir()
        cursor = conectar.cursor()
        sql = "SELECT Pago FROM Tags WHERE Codigo=%s"
        cursor.execute(sql, (str(dato),))
        resultado = cursor.fetchall() 
        conectar.close()
        return resultado
    #Se consulta ultimo ID para guardar siguiente producto
    def devolverMaxIdTags(self):
        conectar = self.abrir()
        cursor = conectar.cursor()
        sql = "SELECT Max(ID) FROM Tags"
        cursor.execute(sql)
        resultado = cursor.fetchall() 
        conectar.close()
        return resultado
    #Se consulta codigo de tag de producto segun ID
    def devolverCodigo(self,dato):
        conectar = self.abrir()
        cursor = conectar.cursor()
        sql = "SELECT Codigo FROM Tags WHERE ID=%s"
        cursor.execute(sql, (dato,))
        resultado = cursor.fetchall() 
        conectar.close()
        return resultado
    #Se consulta datos de producto solicitado
    def devolverProductos(self,dato):
        conectar = self.abrir()
        cursor = conectar.cursor()
        sql = "SELECT ID, Descripcion, Precio, Pago FROM Tags WHERE Descripcion=%s"
        cursor.execute(sql, (str(dato),))
        resultado = cursor.fetchall()
        conectar.close()
        return resultado