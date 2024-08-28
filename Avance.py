import tkinter as tk
from tkinter import ttk, messagebox as mssg
import sqlite3
from datetime import datetime

class DataBaseBuild:
    def __init__(self):
        self.db_name = 'inventario.db'
        self.database_build()
    
    # Crear base de datos
    def database_build(self):  
         # Crear tabla para los proveedores base de datos SQL
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Proveedores (
                    IdNit TEXT PRIMARY KEY,
                    Nombre TEXT,
                    FechaCompra TEXT
                )
            """)
            # Crear tabla para los productos base de datos SQL
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Productos (
                    IdNit TEXT,
                    Codigo TEXT PRIMARY KEY,
                    Nombre TEXT,
                    Unidad TEXT,
                    Cantidad INTEGER,
                    Precio REAL,
                    FechaVencimiento TEXT,
                    FOREIGN KEY(IdNit) REFERENCES Proveedores(IdNit)
                )
            """)
            conn.commit()
    # Operaciones con la base de datos
    def run_Query(self, query, parametros=()):
        ''' Función para ejecutar los Querys a la base de datos '''
        with sqlite3.connect('inventario.db') as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parametros)
            conn.commit()
        return result

    # Insertar base de datos
    def accion_Buscar(self, seleccion, tabla, condicion, valoresdecodicion=()):
        search = f'''SELECT {seleccion} FROM {tabla} WHERE {condicion}'''
        resultado = self.run_Query(search, valoresdecodicion)
        return resultado

    def accion_Eliminar(self, tabla, condicion, valores_de_la_condicion):
        delete = f''' DELETE FROM {tabla} WHERE {condicion} '''
        self.run_Query(delete, valores_de_la_condicion)

    def insertar_Proveedor(self, id, nombre_proveedor, fechaCompra):
        proveedor = [id, nombre_proveedor, fechaCompra]
        self.change_Emptystring_To_Null(proveedor)
        insert = f''' INSERT INTO Proveedores VALUES (?,?,?)'''
        self.run_Query(insert, tuple(proveedor))

    def insertar_Producto(self, IdNit, Codigo, nombreProducto, und, cantidad, precio, fechaVencimiento):
        producto = [IdNit, Codigo, nombreProducto, und, cantidad, precio, fechaVencimiento]
        self.change_Emptystring_To_Null(producto)
        insert = f''' INSERT INTO Productos VALUES (?,?,?,?,?,?,?)'''
        self.run_Query(insert, tuple(producto))

    def actualizar_Proveedor(self, values):
        self.change_Emptystring_To_Null(values)
        update = ''' UPDATE Proveedores 
                    SET Nombre = ? , FechaCompra = ? WHERE 
                    IdNit = ? '''
        self.run_Query(update, tuple(values))

    def actualizar_Producto(self, values):
        self.change_Emptystring_To_Null(values)
        update = ''' UPDATE Productos 
                    SET Nombre = ? , Unidad = ? , Cantidad = ? , Precio = ? , FechaVencimiento = ? 
                    WHERE IdNit = ? AND Codigo = ? '''
        self.run_Query(update, tuple(values))

    def cargar_Proveedor(self, id):
        proveedor = list(self.accion_Buscar("*", "Proveedores", "IdNit = ?", (id,)).fetchall())
        self.change_Nulls_Fetchall(proveedor)
        self.idNit.insert(0, proveedor[0][0])
        self.nombreProveedor.insert(0, proveedor[0][1])
        self.fechaCompra.insert(0, proveedor[0][2])

    def cargar_Producto(self, producto):
        producto = list(producto)
        self.change_Nulls_Fetchone(producto)
        self.codigo.insert(0, producto[1])
        self.nombreProducto.insert(0, producto[2])
        self.unidad.insert(0, producto[3])
        self.cantidad.insert(0, producto[4])
        self.precioCompra.insert(0, producto[5])
        self.borrarFecha()
        self.fechaVencimiento.insert(0, producto[6])

    def change_Nulls_Fetchone(self, lista):
        for item in range(len(lista)):
            if lista[item] is None:
                lista[item] = ''
            lista[item] = str(lista[item])
        return lista

    def change_Nulls_Fetchall(self, lista):
        for item in range(len(lista)):
            lista[item] = list(lista[item])
            self.change_Nulls_Fetchone(lista[item])
        return lista

    def change_Emptystring_To_Null(self, lista):
        for item in range(len(lista)):
            if lista[item] == '':
                lista[item] = None

class DataValidator:
    def __init__(self):
        pass

    # Validaciones del sistema
    def valida_Id_Nit(self, event):
        pass

    def valida_Nombre_Proveedor(self, event):
        pass

    def validaFechaC(self, event):
        pass

    def escribirFechaC(self, event):
        pass

    def borrarFechaC(self):
        pass

    def valida_Codigo(self, event):
        pass

    def valida_Nombre_Producto(self, event):
        pass

    def valida_Unidad(self, event):
        pass

    def valida_Cantidad(self, event):
        pass

    def valida_Precio_Compra(self, event):
        pass

    def validaFechaV(self, event):
        pass

    def escribirFechaV(self, event):
        pass

    def borrarFechaV(self):
        pass

    def validar_ID(self):
        pass

    def validar_Cod(self):
        pass

class MainWindow:
    def __init__(self):
        self.database = DataBaseBuild()
        self.validator = DataValidator()
        self.win = tk.Tk()
        self.win.title("Manejo de Inventario")
        self.init_UI()
    
    def run(self):
        self.win.mainloop()

    # Crear 
    def init_UI(self):
        # Ventana principal
        self.win.geometry('800x600')
        self.win.resizable(False, False)

        # Etiquetas y Entradas de Proveedor
        tk.Label(self.win, text="ID Proveedor").grid(row=0, column=0, padx=10, pady=10, sticky='w')  # Label/widget
        self.idNit = tk.Entry(self.win)     # Label/widget
        self.idNit.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.win, text="Nombre Proveedor").grid(row=1, column=0, padx=10, pady=10, sticky='w')
        self.nombreProveedor = tk.Entry(self.win)
        self.nombreProveedor.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.win, text="Fecha Compra").grid(row=2, column=0, padx=10, pady=10, sticky='w')
        self.fechaCompra = tk.Entry(self.win)
        self.fechaCompra.grid(row=2, column=1, padx=10, pady=10)
        self.reset_fecha(self.fechaCompra)

        # Etiquetas y Entradas de Producto
        tk.Label(self.win, text="Código Producto").grid(row=3, column=0, padx=10, pady=10, sticky='w') # Label/widget
        self.codigo = tk.Entry(self.win)    # Label/widget
        self.codigo.grid(row=3, column=1, padx=10, pady=10)

        tk.Label(self.win, text="Nombre Producto").grid(row=4, column=0, padx=10, pady=10, sticky='w')
        self.nombreProducto = tk.Entry(self.win)
        self.nombreProducto.grid(row=4, column=1, padx=10, pady=10)

        tk.Label(self.win, text="Unidad").grid(row=5, column=0, padx=10, pady=10, sticky='w')
        self.unidad = tk.Entry(self.win)
        self.unidad.grid(row=5, column=1, padx=10, pady=10)

        tk.Label(self.win, text="Cantidad").grid(row=6, column=0, padx=10, pady=10, sticky='w')
        self.cantidad = tk.Entry(self.win)
        self.cantidad.grid(row=6, column=1, padx=10, pady=10)

        tk.Label(self.win, text="Precio Compra").grid(row=7, column=0, padx=10, pady=10, sticky='w')
        self.precioCompra = tk.Entry(self.win)
        self.precioCompra.grid(row=7, column=1, padx=10, pady=10)

        tk.Label(self.win, text="Fecha Vencimiento").grid(row=8, column=0, padx=10, pady=10, sticky='w')
        self.fechaVencimiento = tk.Entry(self.win)
        self.fechaVencimiento.grid(row=8, column=1, padx=10, pady=10)
        self.reset_fecha(self.fechaVencimiento)

        # Botones
        self.btnBuscar = tk.Button(self.win, text="Buscar", command=self.search_Button)
        self.btnBuscar.grid(row=9, column=0, padx=10, pady=10)

        self.btnNuevo = tk.Button(self.win, text="Nuevo", command=self.record_Button)
        self.btnNuevo.grid(row=9, column=1, padx=10, pady=10)

        self.btnCancelar = tk.Button(self.win, text="Cancelar", command=self.cancel_Button_Main_Win)
        self.btnCancelar.grid(row=9, column=2, padx=10, pady=10)

        self.btnEditar = tk.Button(self.win, text="Editar", command=self.edit_Button)
        self.btnEditar.grid(row=10, column=0, padx=10, pady=10)

        self.btnEliminar = tk.Button(self.win, text="Eliminar", command=self.eliminar_Button)
        self.btnEliminar.grid(row=10, column=1, padx=10, pady=10)

        # Treeview para mostrar productos
        self.treeProductos = ttk.Treeview(self.win, columns=("Código", "Nombre", "Unidad", "Cantidad", "Precio", "Vencimiento"), show='headings')
        self.treeProductos.heading("Código", text="Código")
        self.treeProductos.heading("Nombre", text="Nombre")
        self.treeProductos.heading("Unidad", text="Unidad")
        self.treeProductos.heading("Cantidad", text="Cantidad")
        self.treeProductos.heading("Precio", text="Precio")
        self.treeProductos.heading("Vencimiento", text="Vencimiento")
        self.treeProductos.grid(row=11, column=0, columnspan=3, padx=10, pady=10)

        self.treeProductos.bind('<Double-1>', lambda event: self.carga_Datos())

    # Rutina de limpieza de datos
    def limpia_Campos(self):
        self.idNit.delete(0, tk.END)
        self.nombreProveedor.delete(0, tk.END)
        self.fechaCompra.configure(state=tk.NORMAL)
        self.fechaCompra.delete(0, tk.END)
        self.reset_fecha(self.fechaCompra)
        self.codigo.delete(0, tk.END)
        self.nombreProducto.delete(0, tk.END)
        self.unidad.delete(0, tk.END)
        self.cantidad.delete(0, tk.END)
        self.precioCompra.delete(0, tk.END)
        self.fechaVencimiento.configure(state=tk.NORMAL)
        self.fechaVencimiento.delete(0, tk.END)
        self.reset_fecha(self.fechaVencimiento)

    def limpia_Treeview(self):
        for item in self.treeProductos.get_children():   # Obtiene todos los elementos hijos
            self.treeProductos.delete(item)

    def cargar_Datos_Treeview(self, db_rows):
        self.limpia_Treeview()  # Limpiar antes de cargar nuevos datos
        for row in db_rows:
            self.treeProductos.insert('', 0, values=row)
    
    # Acciones
    def search_Button(self):
        search_result = self.database.accion_Buscar("*", "Proveedores", "IdNit = ?", (self.idNit.get(),))
        if search_result:
            self.database.cargar_Proveedor(self.idNit.get())
        else:
            mssg.showerror("Error", "Proveedor no encontrado")

    def record_Button(self):
        self.database.insertar_Proveedor(self.idNit.get(), self.nombreProveedor.get(), self.fechaCompra.get())
        mssg.showinfo("Éxito", "Proveedor registrado exitosamente")

    def cancel_Button_Main_Win(self):
        self.clear_Entries()

    def reset_fecha(self, campo_fecha):
        campo_fecha.configure(foreground="grey")
        campo_fecha.insert(0, 'dd/mm/yyyy')
        campo_fecha.configure(state='readonly')

    def edit_Button(self):
        self.database.actualizar_Proveedor([self.nombreProveedor.get(), self.fechaCompra.get(), self.idNit.get()])
        mssg.showinfo("Éxito", "Proveedor actualizado exitosamente")

    def adiciona_Registro(self, event=None):
        pass

    def carga_Datos(self):
        pass

    def actualizar_datos(self):
        pass

    def eliminar_Button(self):
        # Abre la ventana para confirmar la eliminación del registro seleccionado'''
        if self.tree.selection():
            self.is_open_v_eliminar = True
            self.estado_Buttons_Eliminar(False)
            self.abrir_Ventana_Eliminar()
        else:
            mssg.showerror('Error', '.. No se ha seleccionado ningún registro a eliminar! ..')

    def elimina_Registro(self, obj):
        pass

    def abrir_Ventana_Eliminar(self):
        pass

    def salir_ventana_eliminar(self):
        pass

    def continuar_Button(self):
        pass
    
    def btn_yes (self):
        self.master.elimina_registro()
        self.win.destroy()

    def btn_no(self):
        self.win.destroy()

if __name__ == "__main__":
    app = MainWindow()
    app.run()
