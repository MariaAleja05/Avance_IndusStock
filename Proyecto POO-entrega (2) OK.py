#!/usr/bin/python3
# -*- coding: utf-8 -*-
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox as mssg
import sqlite3
from datetime import datetime

#validar si la fecha es válida
def es_Fecha_Valida(fecha_texto):

   fecha_actual = datetime.now().date()

   espacios = fecha_texto.split('/')
    
   if len(espacios) != 3:
      return False  # La fecha no tiene el formato correcto
    
   dia = espacios[0]
   mes = espacios[1]
   anio = espacios[2]
    
   # Validar el año
   if not (dia.isdigit() and mes.isdigit() and anio.isdigit()):
      return False  # Los componentes no son números
    
   if int(mes) < 1 or int(mes) > 12:
      return False  # Mes fuera de rango
    
   dias_por_mes = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    
   # Verificar si es año bisiesto
   if int(mes) == 2 and ((int(anio) % 4 == 0 and int(anio) % 100 != 0) or (int(anio) % 400 == 0)):
      dias_por_mes[1] = 29
    
   if int(dia) < 1 or int(dia) > dias_por_mes[int(mes) - 1]:
      return False  # Día fuera de rango para el mes dado
   
   fecha_ingresada = datetime(int(anio), int(mes), int(dia)).date()
   if fecha_ingresada < fecha_actual:
      return False  # Si la fecha es pasada
   
   return True  # La fecha es válida

class Inventario:
  def __init__(self, master=None):
    ancho=830
    alto=690 # Dimensiones de la pantalla
    self.ico = r'C:\Users\ayayi\Desktop\f2.png'  # Ruta al archivo de icono
    self.db_name = r'C:\Users\ayayi\Desktop\Inventario.db'  # Ruta a tu base de datos SQLite
    self.actualiza = None
    self.is_open_v_eliminar=None

    # Crea ventana principal
    self.win = tk.Tk() 
    self.win.geometry(f"{ancho}x{alto}")
    self.win.iconbitmap(self.ico) 
    self.win.resizable(True, True)
    self.win.title("Manejo de Inventario") 

    #Centra la pantalla
    self.centra(self.win,ancho,alto)

    # Contenedor de widgets   
    self.win = tk.LabelFrame(master)
    self.win.configure(background="#e0e0e0",font="{Arial} 12 {bold}",
                       height=ancho,labelanchor="n",width=alto)
    self.tabs = ttk.Notebook(self.win)
    self.tabs.configure(height=650, width=799)

    #Frame de datos
    self.frm1 = ttk.Frame(self.tabs)
    self.frm1.configure(height=200, width=200)

    #Etiqueta IdNit del Proveedor
    self.lblIdNit = ttk.Label(self.frm1)
    self.lblIdNit.configure(text='Id/Nit')
    self.lblIdNit.place(anchor="nw", x=10, y=10)

    #Captura IdNit del Proveedor
    self.idNit = ttk.Entry(self.frm1)
    self.idNit.configure(takefocus=True)#, state = 'readonly')
    self.idNit.place(anchor="nw", x=120, y=10)
    self.idNit.bind("<KeyRelease>", self.valida_Id_Nit)
    self.idNit.bind("<BackSpace>", lambda _:self.idNit.delete(len(self.idNit.get())),'end')
    self.idNit.focus_set()

    #Etiqueta nombre del Proveedor
    self.lblNombreProveedor = ttk.Label(self.frm1)
    self.lblNombreProveedor.configure(text='Nombre Proveedor')
    self.lblNombreProveedor.place(anchor="nw", x=10, y=40)

    #Captura nombre del Proveedor
    self.nombreProveedor = ttk.Entry(self.frm1)
    self.nombreProveedor.configure(width=36)
    self.nombreProveedor.place(anchor="nw", x=120, y=40)
    self.nombreProveedor.bind("<KeyRelease>", self.valida_Nombre_Proveedor)
    self.nombreProveedor.bind("<BackSpace>", lambda _:self.nombreProveedor.delete(len(self.nombreProveedor.get())),'end')

    #Etiqueta fecha de compra del Producto
    self.lblFechaCompra = ttk.Label(self.frm1)
    self.lblFechaCompra.configure(text='Fecha Compra')
    self.lblFechaCompra.place(anchor="nw", x=10, y=70)

    #Captura la fecha de compra del Producto
    self.fechaCompra = ttk.Entry(self.frm1)
    self.fechaCompra.configure(width=30, foreground= "gray")
    self.fechaCompra.place(anchor="nw", x=120, y=70)

    self.fechaCompra.insert(0,'dd/mm/yyyy')
    self.fechaCompra.configure(state='readonly')
    self.fechaCompra.bind("<FocusIn>", lambda _: self.borrarFechaC())
    self.fechaCompra.bind("<KeyRelease>", self.escribirFechaC)
    self.fechaCompra.bind("<FocusOut>", self.validaFechaC)
    self.fechaCompra.bind("<BackSpace>", lambda _:self.fechaCompra.delete(len(self.fechaCompra.get())),'end')

    #Separador
    self.separador1 = ttk.Separator(self.frm1)
    self.separador1.configure(orient="horizontal")
    self.separador1.place(anchor="nw", width=800, x=0, y=95)

    #Etiqueta Código del Producto
    self.lblCodigo = ttk.Label(self.frm1)
    self.lblCodigo.configure(text='Código')
    self.lblCodigo.place(anchor="nw", x=10, y=100)

    #Captura el código del Producto
    self.codigo = ttk.Entry(self.frm1)
    self.codigo.configure(width=13)# state = 'readonly')
    self.codigo.place(anchor="nw", x=120, y=100)
    self.codigo.bind("<KeyRelease>", self.valida_Codigo)
    self.codigo.bind("<BackSpace>", lambda _:self.codigo.delete(len(self.codigo.get())),'end')

    #Etiqueta el nombre del Producto
    self.lblNombreProducto= ttk.Label(self.frm1)
    self.lblNombreProducto.configure(text='Nombre Producto')
    self.lblNombreProducto.place(anchor="nw", x=10, y=130)

    #Captura el nombre del Producto
    self.nombreProducto = ttk.Entry(self.frm1)
    self.nombreProducto.configure(width=36)
    self.nombreProducto.place(anchor="nw", x=120, y=130)
    self.nombreProducto.bind("<KeyRelease>", self.valida_Nombre_Producto)
    self.nombreProducto.bind("<BackSpace>", lambda _:self.nombreProducto.delete(len(self.nombreProducto.get())),'end')

    #Etiqueta precio del Producto
    self.lblPrecioCompra = ttk.Label(self.frm1)
    self.lblPrecioCompra.configure(text='Precio Compra $')
    self.lblPrecioCompra.place(anchor="nw", x=10, y=160)

    #Captura el precio del Producto
    self.precioCompra = ttk.Entry(self.frm1)
    self.precioCompra.configure(width=15)
    self.precioCompra.place(anchor="nw", x=120, y=160)
    self.precioCompra.bind("<KeyRelease>", self.valida_Precio_Compra)
    self.precioCompra.bind("<BackSpace>", lambda _:self.precioCompra.delete(len(self.precioCompra.get())),'end')

    #Etiqueta fecha de vencimiento del Producto
    self.lblFechaVencimiento = ttk.Label(self.frm1)
    self.lblFechaVencimiento.configure(text='Fecha Vencimiento')
    self.lblFechaVencimiento.place(anchor="nw", x=10, y=190)

    #Captura la fecha de vencimiento del Producto
    self.fechaVencimiento = ttk.Entry(self.frm1)
    self.fechaVencimiento.configure(width=30, foreground= "gray")
    self.fechaVencimiento.place(anchor="nw", x=120, y=190)

    self.fechaVencimiento.insert(0,'dd/mm/yyyy')
    self.fechaVencimiento.configure(state='readonly')
    self.fechaVencimiento.bind("<FocusIn>", lambda _: self.borrarFechaV())
    self.fechaVencimiento.bind("<KeyRelease>", self.escribirFechaV)
    self.fechaVencimiento.bind("<FocusOut>", self.validaFechaV)
    self.fechaVencimiento.bind("<BackSpace>", lambda _:self.fechaVencimiento.delete(len(self.fechaVencimiento.get())),'end')
  
    #Etiqueta unidad o medida del Producto
    self.lblUnd = ttk.Label(self.frm1)
    self.lblUnd.configure(text='Unidad')
    self.lblUnd.place(anchor="nw", x=10, y=220)

    #Captura la unidad o medida del Producto
    self.unidad = ttk.Entry(self.frm1)
    self.unidad.configure(width=10)
    self.unidad.place(anchor="nw", x=120, y=220)
    self.unidad.bind("<KeyRelease>", self.valida_Unidad)
    self.unidad.bind("<BackSpace>", lambda _:self.unidad.delete(len(self.unidad.get())),'end')

    #Etiqueta cantidad del Producto
    self.lblCantidad = ttk.Label(self.frm1)
    self.lblCantidad.configure(text='Cantidad')
    self.lblCantidad.place(anchor="nw", x=10, y=250)

    #Captura la cantidad del Producto
    self.cantidad = ttk.Entry(self.frm1)
    self.cantidad.configure(width=12)
    self.cantidad.place(anchor="nw", x=120, y=250)
    self.cantidad.bind("<KeyRelease>", self.valida_Cantidad)
    self.cantidad.bind("<BackSpace>", lambda _:self.cantidad.delete(len(self.cantidad.get())),'end')

    #Separador
    self.separador2 = ttk.Separator(self.frm1)
    self.separador2.configure(orient="horizontal")
    self.separador2.place(anchor="nw", width=800, x=0, y=280)

    #tablaTreeView
    self.style=ttk.Style()
    self.style.configure("estilo.Treeview", highlightthickness=0, bd=0, background="#e0e0e0", font=('Calibri Light',10))
    self.style.configure("estilo.Treeview.Heading", background='Azure', font=('Calibri Light', 10,'bold')) 
    self.style.layout("estilo.Treeview", [('estilo.Treeview.treearea', {'sticky': 'nswe'})])
    
    #Árbol para mosrtar los datos de la B.D.
    self.treeProductos = ttk.Treeview(self.frm1, style="estilo.Treeview")
    self.treeProductos.configure(selectmode="extended")
    self.treeProductos.bind('<Double-Button-1>',lambda _: self.carga_Datos())

    # Etiquetas de las columnas para el TreeView
    self.treeProductos["columns"]=("Codigo","Nombre_Producto","Und","Cantidad","Precio","Fecha_Vencimiento")
    # Características de las columnas del árbol
    self.treeProductos.column ("#0",          anchor="w",stretch=True,width=3)
    self.treeProductos.column ("Codigo",      anchor="w",stretch=True,width=3)
    self.treeProductos.column ("Nombre_Producto", anchor="w",stretch=True,width=150)
    self.treeProductos.column ("Und",         anchor="w",stretch=True,width=3)
    self.treeProductos.column ("Cantidad",    anchor="w",stretch=True,width=3)
    self.treeProductos.column ("Precio",      anchor="w",stretch=True,width=8)
    self.treeProductos.column ("Fecha_Vencimiento",       anchor="w",stretch=True,width=3)

    # Etiquetas de columnas con los nombres que se mostrarán por cada columna
    self.treeProductos.heading("#0",          anchor="center", text='ID / Nit')
    self.treeProductos.heading("Codigo",      anchor="center", text='Código')
    self.treeProductos.heading("Nombre_Producto", anchor="center", text='Nombre_Producto')
    self.treeProductos.heading("Und",         anchor="center", text='Unidad')
    self.treeProductos.heading("Cantidad",    anchor="center", text='Cantidad')
    self.treeProductos.heading("Precio",      anchor="center", text='Precio')
    self.treeProductos.heading("Fecha_Vencimiento",       anchor="center", text='Fecha_Vencimiento')

    #Carga los datos en treeProductos
    self.treeProductos.place(anchor="nw", height=400, width=790, x=2, y=290)

    #Scrollbar en el eje Y de treeProductos
    self.scrollbary=ttk.Scrollbar(self.treeProductos, orient='vertical', command=self.treeProductos.yview)
    self.treeProductos.configure(yscroll=self.scrollbary.set)
    self.scrollbary.place(x=778, y=25, height=478)

    # Título de la pestaña Ingreso de Datos
    self.frm1.pack(side="top")
    self.tabs.add(self.frm1, compound="center", text='Ingreso de inventario')
    self.tabs.pack(side="top")

    #Frame 2 para contener los botones
    self.frm2 = ttk.Frame(self.win)
    self.frm2.configure(height=50, width=800)

    #Botón para Buscar un Proveedor
    self.btnBuscar = ttk.Button(self.frm2)
    self.btnBuscar.configure(text='Busca',command= self.search_Button)
    self.btnBuscar.place(anchor="nw", width=70, x=200, y=20)

    #Botón para Guardar los datos
    self.btnGuardar = ttk.Button(self.frm2)
    self.btnGuardar.configure(text='Guardar', command= self.record_Button)
    self.btnGuardar.place(anchor="nw", width=70, x=275, y=20)

    #Botón para Editar los datos
    self.btnEditar = ttk.Button(self.frm2)
    self.btnEditar.configure(text='Editar', command=self.carga_Datos)
    self.btnEditar.place(anchor="nw", width=70, x=350, y=20)

    #Botón para Elimnar datos
    self.btnEliminar = ttk.Button(self.frm2)
    self.btnEliminar.configure(text='Eliminar', command= self.eliminar_Button)
    self.btnEliminar.place(anchor="nw", width=70, x=425, y=20)

    #Botón para cancelar una operación
    self.btnCancelar = ttk.Button(self.frm2)
    self.btnCancelar.configure(text='Cancelar', width=80, command = self.cancel_Button_Main_Win)
    self.btnCancelar.place(anchor="nw", width=70, x=500, y=20)

    #Ubicación del Frame 2
    self.frm2.place(anchor="nw", height=60, relwidth=1, y=605)
    self.win.pack(anchor="center", side="top")

    # widget Principal del sistema
    self.mainwindow = self.win

  #Fución de manejo de eventos del sistema
  
  def database_build(self):
     producto=''' CREATE TABLE IF NOT EXISTS "Productos" (
	  "IdNit"	VARCHAR(15) NOT NULL,
	  "Codigo"	VARCHAR(15) NOT NULL,
	  "Nombre_Producto"	VARCHAR,
	  "Und"	VARCHAR(10),
	  "Cantidad"	DOUBLE,
	  "Precio"	DOUBLE,
	  "Fecha_Vencimiento"	DATE,
	  PRIMARY KEY("Codigo","IdNit") ) '''
     proveedor='''CREATE TABLE IF NOT EXISTS "Proveedores" (
	  "idNitProv"	VARCHAR NOT NULL UNIQUE,
	  "Nombre_Proveedor"	VARCHAR,
	  "Fecha_Compra"	VARCHAR,
	  PRIMARY KEY("idNitProv") )'''
     self.run_Query(proveedor)
     self.run_Query(producto)

  def run(self):
      self.database_build()
      self.mainwindow.mainloop()

  ''' ......... Métodos utilitarios del sistema .............'''
  #Rutina de centrado de pantalla
  def centra(self,win,ancho,alto): 
      """ centra las ventanas en la pantalla """ 
      x = win.winfo_screenwidth() // 2 - ancho // 2 
      y = win.winfo_screenheight() // 2 - alto // 2 
      win.geometry(f'{ancho}x{alto}+{x}+{y}') 
      win.deiconify() # Se usa para restaurar la ventana
   
 # Validaciones del sistema
  def valida_Id_Nit(self, event):
    ''' Valida que la longitud no sea mayor a 15 caracteres'''
    if event.char:
      if ' ' in self.idNit.get():
            mssg.showerror("Error", "No se permiten espacios.")
            
            # Eliminar el espacio ingresado
            contenido_sin_espacio = self.idNit.get().replace(' ', '')
            # Establecer el contenido sin espacios en el Entry
            self.idNit.delete(0, tk.END)
            self.idNit.insert(0, contenido_sin_espacio)

      if len(self.idNit.get()) > 15:
         self.idNit.delete(15,tk.END)
         mssg.showerror('Atención!!','.. ¡Máximo 15 caracteres! ..')

  def valida_Nombre_Proveedor(self, event):
     ''' Valida que la longitud no sea mayor a 25 caracteres'''
     if event.char:
        if len(self.nombreProveedor.get()) > 25:
           self.nombreProveedor.delete(25,tk.END)
           mssg.showerror('Atención!!','.. ¡Máximo 25 caracteres! ..')
          
  def validaFechaC(self, event):  
      '''Valida que la fecha sea válida o pone el fomato de fecha'''
      if event.char:
         if es_Fecha_Valida(self.fechaCompra.get()) == False and self.fechaCompra.get()!= '':
            mssg.showerror('Atención!!','.. ¡Fecha Inválida! ..')
            self.fechaCompra.delete(0, tk.END)
         if len(self.fechaCompra.get())==0:
            self.fechaCompra.configure(foreground= "grey")
            self.fechaCompra.insert(0, 'dd/mm/yyyy')
            self.fechaCompra.configure(state='readonly')

  def escribirFechaC(self, event):
    #para que solo se ejecute si escribe números y tiene menos de diez caracteres
    fechaCompra=self.fechaCompra.get()
    if event.char.isdigit() and len(self.fechaCompra.get())<=10:
        
        letras = 0
        for i in fechaCompra:
            letras +=1

        if letras == 2:
            self.fechaCompra.insert(2,"/")
        elif letras == 5:
            self.fechaCompra.insert(5,"/")
    elif len(fechaCompra)>10:
       self.fechaCompra.delete(10, tk.END)
       mssg.showerror('.. Error! ..', 'Limite de caracteres excedido, fecha invalida')
    elif fechaCompra !='dd/mm/yyyy' or fechaCompra != '':
       condicion_fechaCompra=None
       partes_fechaCompra=fechaCompra.split('/')
       for part in partes_fechaCompra:
          if part.isdigit() or part=='':
             condicion_fechaCompra=True
          else:
             condicion_fechaCompra=False
             break
       if len(partes_fechaCompra)>3 or condicion_fechaCompra==False:
          self.fechaCompra.delete(0,tk.END)
          mssg.showerror(' .. Error! ..','  ¡Fecha invalida!  ')
          
  def borrarFechaC(self):

   if self.fechaCompra.get()=="dd/mm/yyyy":
      self.fechaCompra.configure(state="normal")
      self.fechaCompra.delete(0, tk.END)
      self.fechaCompra.config(foreground='black')
          
  def valida_Codigo(self, event):
     ''' Valida que la longitud no sea mayor a 15 caracteres'''
     if event.char:
        if ' ' in self.codigo.get():
            mssg.showerror("Error", "No se permiten espacios.")
            
            # Eliminar el espacio ingresado
            contenido_sin_espacio = self.codigo.get().replace(' ', '')
            # Establecer el contenido sin espacios en el Entry
            self.codigo.delete(0, tk.END)
            self.codigo.insert(0, contenido_sin_espacio)

        if len(self.codigo.get()) > 15:
           self.codigo.delete(15,tk.END)
           mssg.showerror('Atención!!','.. ¡Máximo 15 caracteres! ..')

  def valida_Nombre_Producto(self, event):
     ''' Valida que la longitud no sea mayor a 50 caracteres'''
     if event.char:
        if len(self.nombreProducto.get()) > 50:
           self.nombreProducto.delete(50,'end')
           mssg.showerror('Atención!!','.. ¡Máximo 50 caracteres! ..')
 
  def valida_Unidad(self, event):
     ''' Valida que la longitud no sea mayor a 10 caracteres'''
     if event.char:
        if len(self.unidad.get()) > 10:
           self.unidad.delete(10,tk.END)
           mssg.showerror('Atención!!','.. ¡Máximo 10 caracteres! ..')

  def valida_Cantidad(self, event):
     ''' Valida que la longitud no sea mayor a 6 caracteres y sea int'''
     if event.char:
        if len(self.cantidad.get()) > 6:
            self.cantidad.delete(6,tk.END)
            mssg.showerror('Atención!!','.. ¡Máximo 6 caracteres! ..')
             
        try:
           float_numero=float(self.cantidad.get())
        except ValueError:
           mssg.showerror( '.. Error! ..', ' ¡Cantidad invalida!')
           self.cantidad.delete(0,tk.END)
  
  def valida_Precio_Compra(self, event):
    ''' Valida que la longitud no sea mayor a 9 caracteres y sea int'''
    if event.char:
        if len(self.precioCompra.get()) > 9:
            self.precioCompra.delete(9,tk.END)
            mssg.showerror('Atención!!','.. ¡Máximo 9 caracteres! ..')

    # Intentar convertir el contenido en un número
    try:
        float_numero = float(self.precioCompra.get())
    except ValueError:
        mssg.showerror('Atención!!','.. ¡Precio inválido! ..')
        self.precioCompra.delete(0, tk.END)  # Limpiar el contenido del Entry en caso de error              
            
  def validaFechaV(self, event):  
      '''Valida que la fecha sea válida o pone el fomato de fecha'''
      if event.char:
         if es_Fecha_Valida(self.fechaVencimiento.get()) == False and self.fechaVencimiento.get()!= '':
            mssg.showerror('Atención!!','.. ¡Fecha Inválida! ..')
            self.fechaVencimiento.delete(0, tk.END)
         if len(self.fechaVencimiento.get())==0:
            self.fechaVencimiento.configure(foreground= "grey")
            self.fechaVencimiento.insert(0, 'dd/mm/yyyy')
            self.fechaVencimiento.configure(state='readonly')

  def escribirFechaV(self, event):
    #para que solo se ejecute si escribe números y tiene menos de diez caracteres
    fechaVencimiento=self.fechaVencimiento.get()
    if event.char.isdigit() and len(self.fechaVencimiento.get())<=10:
        
        letras = 0
        for i in fechaVencimiento:
            letras +=1

        if letras == 2:
            self.fechaVencimiento.insert(2,"/")
        elif letras == 5:
            self.fechaVencimiento.insert(5,"/")
    elif len(fechaVencimiento)>10:
       self.fechaVencimiento.delete(10, tk.END)
       mssg.showerror('.. Error! ..', 'Limite de caracteres excedido, fecha invalida')
    elif fechaVencimiento !='dd/mm/yyyy' or fechaVencimiento != '':
       condicion_fechaVencimiento=None
       partes_fechaVencimiento=fechaVencimiento.split('/')
       for part in partes_fechaVencimiento:
          if part.isdigit() or part=='':
             condicion_fechaVencimiento=True
          else:
             condicion_fechaVencimiento=False
             break
       if len(partes_fechaVencimiento)>3 or condicion_fechaVencimiento==False:
          self.fechaVencimiento.delete(0,tk.END)
          mssg.showerror(' .. Error! ..','  ¡Fecha invalida!  ')
          
  def borrarFechaV(self):

   if self.fechaVencimiento.get()=="dd/mm/yyyy":
      self.fechaVencimiento.configure(state="normal")
      self.fechaVencimiento.delete(0, tk.END)
      self.fechaVencimiento.config(foreground='black')
   
  def validar_ID(self):
     id=self.idNit.get()
     search_id=self.accion_Buscar('*','Proveedores','idNitProv= ? ', (id,)).fetchone()
     if search_id==None :
        prov_Exist=False
     else:
        prov_Exist=True
     return prov_Exist
  
  def validar_Cod(self):
     codigo=self.codigo.get()
     search_id=self.accion_Buscar('*','Productos','Codigo= ? ', (codigo,)).fetchone()
     if search_id==None :
        cod_Exist=False
     else:
        cod_Exist=True
     return cod_Exist
        
  #Rutina de limpieza de datos
  def limpia_Campos(self):
      ''' Limpia todos los campos de captura'''
      self.idNit.configure(state = 'normal')
      self.idNit.delete(0,'end')
      self.nombreProveedor.delete(0,'end')
      self.fechaCompra.delete(0,'end')
      self.idNit.delete(0,'end')
      self.codigo.configure(state = 'normal')
      self.codigo.delete(0,'end')
      self.nombreProducto.delete(0,'end')
      self.unidad.delete(0,'end')
      self.cantidad.delete(0,'end')
      self.precioCompra.delete(0,'end')
      self.fechaVencimiento.delete(0,'end')
      
  def limpiar_Treeview(self):
    tabla_TreeView = self.treeProductos.get_children()
    for linea in tabla_TreeView:
        self.treeProductos.delete(linea)

  def cargar_Datos_Treeview(self,db_rows):
      self.change_Nulls_Fetchall(db_rows)
      for row in db_rows:
         self.treeProductos.insert('',0, text = row[0], values = [row[1],row[2],row[3],row[4],row[5],row[6]])       
           
  # Operaciones con la base de datos
  def run_Query(self, query, parametros = ()):
    ''' Función para ejecutar los Querys a la base de datos '''
    with sqlite3.connect(self.db_name) as conn:
        cursor = conn.cursor()
        result = cursor.execute(query, parametros)
        conn.commit()
    return result
          
  def accion_Buscar(self,seleccion,tabla,condicion, valoresdecodicion =()):
    search=f'''SELECT {seleccion} FROM {tabla} WHERE {condicion}'''
    resultado=self.run_Query(search,valoresdecodicion)
    return resultado
  
  def accion_Eliminar(self, tabla, condicion, valores_de_la_condicion):
     delete=f''' DELETE FROM {tabla} WHERE {condicion} '''
     self.run_Query(delete, valores_de_la_condicion)
  
  def insertar_Proveedor(self, id , nombre_proveedor, fechaCompra):
    proveedor=[id,nombre_proveedor,fechaCompra]
    self.change_Emptystring_To_Null(proveedor)
    insert=f''' INSERT INTO Proveedores VALUES (?,?,?)'''
    self.run_Query(insert, tuple(proveedor))
   
  def insertar_Producto(self, IdNit, Codigo, nombreProducto, und, cantidad, precio, fechaVencimiento):
    producto=[IdNit, Codigo, nombreProducto, und, cantidad, precio, fechaVencimiento]
    self.change_Emptystring_To_Null(producto)
    insert=f''' INSERT INTO Productos VALUES (?,?,?,?,?,?,?)'''
    self.run_Query(insert, tuple(producto))

  def actualizar_Proveedor(self, values):
     self.change_Emptystring_To_Null(values)
     update=''' UPDATE Proveedores 
                SET Nombre_Proveedor = ? , Fecha_Compra = ? WHERE 
                idNitProv = ? '''
     self.run_Query(update,tuple(values))

  def actualizar_Producto(self,values):
     self.change_Emptystring_To_Null(values)
     update=''' UPDATE Productos 
             SET Nombre_Producto = ? , Und = ? , Cantidad = ? , Precio_Compra = ? , Fecha_Vencimiento = ? 
             WHERE IdNit = ? AND Codigo = ? '''
     self.run_Query(update,tuple(values))
  
  def cargar_Proveedor(self, id):
     proveedor=list(self.accion_Buscar("*","Proveedores","idNitProv= ? " , (id,)).fetchall())
     self.change_Nulls_Fetchall(proveedor)
     self.idNit.insert(0,proveedor[0][0])
     self.nombreProveedor.insert(0,proveedor[0][1])
     self.fechaCompra.insert(0, proveedor[0][2])
  
  def cargar_Producto(self,producto):
     producto=list(producto)
     self.change_Nulls_Fetchone(producto)
     self.codigo.insert(0,producto[1])
     self.nombreProducto.insert(0,producto[2])
     self.unidad.insert(0,producto[3])
     self.cantidad.insert(0,producto[4])
     self.precioCompra.insert(0,producto[5])
     self.borrarFecha()
     self.fechaVencimiento.insert(0,producto[6])

  def change_Nulls_Fetchone(self,lista):
     for item in range(len(lista)):
        if lista[item]==None:
           lista[item]=''
        lista[item]=str(lista[item])
     return lista
   
  def change_Nulls_Fetchall(self, lista):
     for item in range(len(lista)):
        lista[item]=list(lista[item])
        self.change_Nulls_Fetchone(lista[item])
     return lista
  
  def change_Emptystring_To_Null(self,lista):
     for item in range(len(lista)):
        if lista[item]=='':
           lista[item]=None

  def search_Button (self):
     id= self.idNit.get()
     cod= self.codigo.get()
     if id=='' and cod == '':
        mssg.showinfo('Atención', ' No se ha ingresado nada para buscar')
     elif id != "" and cod =="":
        if self.validar_ID()==True:
          search=self.accion_Buscar("*","Productos", "IdNit= ? ", (id,)).fetchall()
          self.limpia_Campos()
          self.cargar_Datos_Buscados(search)
          self.cargar_Proveedor(id)
        else:
           mssg.showerror('Atención!!','.. ¡El proveedor no existe! ..')
     elif id == "" and cod !="":
        if self.validar_Cod()==True:
           search=self.accion_Buscar("*","Productos", "Codigo= ? ",(cod,)).fetchall()
           self.cargar_Datos_Buscados(search)
           self.limpia_Campos()
           if len(search)>1:
              self.codigo.insert(0,cod)
           else:
              self.cargar_Producto(search[0])
              self.cargar_Proveedor(search[0][0])
        else:
           mssg.showerror('Atención!!','.. ¡El producto no existe! ..')
     elif id != "" and cod !="":
        if self.validar_ID()==True and self.validar_Cod()==True:
           search=self.accion_Buscar("*","Productos", "Codigo= ? AND IdNit= ? ", (cod , id,)).fetchall()
           if search == []:
              mssg.showerror('Atención!!','.. ¡El producto no corresponde al proveedor indicado! ..')
           else: 
              self.limpia_Campos()
              self.cargar_Datos_Buscados(search)
              self.cargar_Proveedor(id)
              self.cargar_Producto(search[0])
        elif self.validar_ID()==True and self.validar_Cod()==False:
           mssg.showerror('Atención!!','.. ¡El producto no existe! ..')
        elif self.validar_ID()==False and self.validar_Cod()==True:
           mssg.showerror('Atención!!','.. ¡El proveedor no existe! ..')
        elif self.validar_ID()==False and self.validar_Cod()==False:
           mssg.showerror('Atención!!','.. ¡Ni el producto, ni el proveedor existen! ..')

  def cargar_Datos_Buscados(self,search):
      self.limpiar_Treeview()
      self.cargar_Datos_Treeview(search)

  def cancel_Button_Main_Win(self):
     self.limpiar_Treeview()
     self.limpia_Campos()
     self.fechaCompra.configure(foreground= "grey")
     self.fechaCompra.insert(0, 'dd/mm/yyyy')
     self.fechaCompra.configure(state='readonly')
     self.fechaVencimiento.configure(foreground= "grey")
     self.fechaVencimiento.insert(0, 'dd/mm/yyyy')
     self.fechaVencimiento.configure(state='readonly')
     if self.actualiza == True:
         self.actualiza = None
         mssg.showinfo(".. Confirmación ..", '.. Ha salido del modo Editar ..')
     self.estado_Buttons_Eliminar(True)
     if self.is_open_v_eliminar==True:
         self.salir_ventana_eliminar()
   
  def record_Button(self):
     if self.actualiza==None:
        self.adiciona_Registro()
     elif self.actualiza== True:
        self.actualizar_datos()
        self.estado_Buttons_Editar(True)

  def adiciona_Registro(self, event=None):
    '''Adiciona un producto a la BD si la validación es True'''
    # Obtener los valores de los campos de entrada
    id_nit = self.idNit.get()
    nombre_proveedor = self.nombreProveedor.get()
    fecha_compra = self.fechaCompra.get()
    codigo = self.codigo.get()
    nombre_producto = self.nombreProducto.get()
    unidad = self.unidad.get()
    cantidad = self.cantidad.get()
    precio_compra = self.precioCompra.get()
    fecha_vencimiento = self.fechaVencimiento.get()
    relacion=self.accion_Buscar('*','Productos','IdNit = ? AND Codigo = ?',(id_nit, codigo,)).fetchone()

    if id_nit=="" and codigo=="":
       mssg.showerror('Atención!!','.. ¡No se ha especificado ningún dato para guardar! ..')

    elif id_nit=="" and codigo!="":
       mssg.showerror('Atención!!','.. ¡No se especificó ningún proveedor para el producto! ..')

    elif codigo=="" and id_nit!= "":
       
       if self.validar_ID()==False:
          self.insertar_Proveedor(id_nit, nombre_proveedor,fecha_compra)
          mssg.showinfo('Confirmación','.. El proveedor ha sido registrado correctamente ..')

       elif self.validar_ID()==True:
          mssg.showerror('Atención!!','.. ¡El proveedor ya existe y no puede ser insertado otra vez! ..')

    elif id_nit!="" and codigo!="":
       if fecha_compra!="" and fecha_compra != 'dd/mm/yyyy':
          if (self.validar_ID()==False and self.validar_Cod()==False) or (self.validar_Cod()==True and self.validar_ID()==False):
             self.insertar_Proveedor(id_nit,nombre_proveedor,fecha_compra)
             mssg.showinfo('Confirmación','.. El proveedor ha sido registrado correctamente ..')
             self.insertar_Producto(id_nit,codigo,nombre_producto,unidad,cantidad, precio_compra, fecha_vencimiento)
             mssg.showinfo('Confirmación','.. El producto ha sido registrado correctamente ..')
             datos=self.accion_Buscar("*","Productos"," IdNit = ? AND Codigo = ?",(id_nit,codigo,)).fetchall()
             self.cargar_Datos_Buscados(datos)

          elif (self.validar_ID()==True and self.validar_Cod()==False) or (relacion == None):
          
             self.insertar_Producto(id_nit,codigo,nombre_producto,unidad,cantidad, precio_compra, fecha_vencimiento)
             mssg.showinfo('Confirmación','.. El producto ha sido registrado correctamente ..')
             datos=self.accion_Buscar("*","Productos"," IdNit = ? AND Codigo = ?",(id_nit,codigo,)).fetchall()
             self.cargar_Datos_Buscados(datos)

          elif relacion!= None:  
             mssg.showerror('Atención!!','.. ¡El producto ya está relacionado con el proveedor indicado! ..')
       elif fecha_compra=="":
            mssg.showerror('Atención!!','.. ¡Digite una fecha para registrar! ..')
  
  def carga_Datos(self):
    seleccion=self.treeProductos.selection()
    if seleccion != ():
       self.estado_Buttons_Editar(False)
       self.limpia_Campos()
       item=self.treeProductos.item(seleccion)
       self.cargar_Proveedor(item ['text'])
       self.idNit.configure(state = 'readonly')
       self.codigo.insert(0,item['values'][0])
       self.codigo.configure(state='readonly')
       self.nombreProducto.insert(0,item['values'][1])
       self.unidad.insert(0,item['values'][2])
       self.cantidad.insert(0,item['values'][3])
       self.precioCompra.insert(0,item['values'][4])
       self.borrarFechaV()
       self.fechaVencimiento.insert(0,item['values'][5])
       self.actualiza=True
       dato_cargado=[[item['text'],item['values'][0],item['values'][1],item['values'][2],item['values'][3],item['values'][4],item['values'][5]]]
       self.cargar_Datos_Buscados(dato_cargado)
       mssg.showinfo('Confirmación',
                     '''.. Se ha activado el modo Editar, puede modificar la información del producto y proveedor seleccionado ..''')
    elif seleccion== ():
       mssg.showerror('Atención!!','.. ¡No se ha seleccionado nada! ..')

  def estado_Buttons_Editar(self, estado):
     if estado==True:
        self.btnBuscar.configure(state='normal')
        self.btnEditar.configure(state='normal')
        self.btnEliminar.configure(state='normal')
     elif estado==False:
        self.btnBuscar.configure(state='disabled')
        self.btnEditar.configure(state='disabled')
        self.btnEliminar.configure(state='disabled')

  def actualizar_datos(self):
     id_nit = self.idNit.get()
     nombre_proveedor = self.nombreProveedor.get()
     fecha_compra = self.fechaCompra.get()
     codigo = self.codigo.get()
     nombre_producto = self.nombreProducto.get()
     unidad = self.unidad.get()
     cantidad = self.cantidad.get()
     precio_compra = self.precioCompra.get()
     fecha_vencimiento = self.fechaVencimiento.get()
     proveedor=self.change_Nulls_Fetchone(list(self.accion_Buscar('*', 'Proveedores', ' idNitProv = ? ', (id_nit,)).fetchone()))
     producto=self.change_Nulls_Fetchone(list(self.accion_Buscar('*', 'Productos', ' IdNit = ? AND Codigo = ? ', (id_nit, codigo,)).fetchone()))
     proveedor_update=[id_nit,nombre_proveedor,fecha_compra]
     producto_update=[id_nit,codigo,nombre_producto,unidad,cantidad,precio_compra,fecha_vencimiento]
     if proveedor == proveedor_update:
        if producto==producto_update:
           mssg.showinfo('.. Confirmación ..', '.. No se realizó ningún cambio, saliendo del modo Editar ..')
        elif producto!=producto_update:
           self.actualizar_Producto([nombre_producto,unidad,cantidad,precio_compra,fecha_vencimiento,id_nit,codigo])
           self.cargar_Datos_Buscados([[id_nit,codigo,nombre_producto,unidad,cantidad,precio_compra,fecha_vencimiento]])
           mssg.showinfo('.. Confirmación ..', '.. Producto actualizado ..')
     elif proveedor!=proveedor_update:
        self.actualizar_Proveedor([nombre_proveedor,fecha_compra,id_nit])
        mssg.showinfo('.. Confirmación ..', '.. Proveedor actualizado ..')   
        if producto!=producto_update:
           self.actualizar_Producto([nombre_producto,unidad,cantidad,precio_compra,fecha_vencimiento,id_nit,codigo])
           self.cargar_Datos_Buscados([[id_nit,codigo,nombre_producto,unidad,cantidad,precio_compra,fecha_vencimiento]])
           mssg.showinfo('.. Confirmación ..', '.. Producto actualizado ..')
     self.actualiza=None
     self.limpia_Campos()

  def eliminar_Button(self):
     if self.treeProductos.selection() != (): 
        self.is_open_v_eliminar=True
        self.estado_Buttons_Eliminar(False)
        self.abrir_Ventana_Eliminar()
     elif self.treeProductos.selection()==():
        mssg.showerror('.. Error!..', ' .. No se ha seleccionado ningún registro a eliminar! .. ')

  def estado_Buttons_Eliminar(self,estado):
     if estado==False:
        self.btnBuscar.configure(state='disabled')
        self.btnGuardar.configure(state='disabled')
        self.btnEditar.configure(state='disabled')
        self.btnEliminar.configure(state='disabled')
     elif estado==True:
        self.btnBuscar.configure(state='normal')
        self.btnGuardar.configure(state='normal')
        self.btnEditar.configure(state='normal')
        self.btnEliminar.configure(state='normal')

  def elimina_Registro(self, obj):
    '''Elimina un Registro en la BD'''
    id=obj["text"]
    codigo=obj["values"][0]
    if self.obj_eliminar.get()=='Producto':
       try:
          self.accion_Eliminar('Productos','IdNit = ? AND Codigo = ? ',(id, codigo,))
       except:
          mssg.showerror('.. Error! ..', f'Se ha producido un error al tratar de eliminar el registro del producto {codigo}, correspondiente al proveedor {id}')
       else:
          mssg.showinfo(' .. Confirmación .. ', f'Se ha eliminado el registro del producto {codigo}, correspondiente al proveedor {id} correctamente')
    elif self.obj_eliminar.get()=='Proveedor':
       try:
          self.accion_Eliminar('Productos','IdNit = ? ',(id,))
          self.accion_Eliminar('Proveedores','idNitProv = ? ', (id,))
       except:
          mssg.showerror('.. Error! ..', f'Se ha producido un error al tratar de eliminar el proveedor {id} y todos los registros relacionados a él')
       else:
          mssg.showinfo(' .. Confirmación .. ', f'Se ha eliminado el proveedor {id} y todos los registros relacionados a él correctamente')
    elif self.obj_eliminar.get()=='Todos los productos':
       try:
          self.accion_Eliminar('Productos','Codigo = ? ',(codigo,))
       except:
          mssg.showerror('.. Error! ..', f'Se ha producido un error al tratar de eliminar todos los registros relacionados con el producto {codigo}')
       else:
          mssg.showinfo(' .. Confirmación .. ', f'Se ha eliminado todos los registros relacionados al producto {codigo}')      

  def abrir_Ventana_Eliminar(self):
     # Crear una ventana secundaria usando toplevel
     self.ventana_eliminar = tk.Toplevel(self.win)
     self.ventana_eliminar.configure(
            background="#afafaf",
            padx=10,
            pady=30)
     self.ventana_eliminar.protocol("WM_DELETE_WINDOW", lambda: None)
     self.ventana_eliminar.iconbitmap(self.ico)
     self.ventana_eliminar.resizable(False, False)
     self.ventana_eliminar.title("Eliminar")

     self.frame_eliminar_1 = ttk.Frame(self.ventana_eliminar)
     self.frame_eliminar_1.place(
            anchor="center",
            height=200,
            width=250,
            x=165,
            y=100)

     self.obj_eliminar = tk.StringVar()

     self.radiobutton1 = ttk.Radiobutton(self.frame_eliminar_1)
     self.radiobutton1.configure(
            text='Eliminar eL Producto \nseleccionado',
            value="Producto",
            variable=self.obj_eliminar)
     self.radiobutton1.place(anchor="w", height=50, x=10, y=50)
     
     self.radiobutton2 = ttk.Radiobutton(self.frame_eliminar_1)
     self.radiobutton2.configure(
            text='Eliminar Proveedor y todos sus \nproductos',
            value="Proveedor",
            variable=self.obj_eliminar)
     self.radiobutton2.place(anchor="w", x=10, y=95)

     self.radiobutton3 = ttk.Radiobutton(self.frame_eliminar_1)
     self.radiobutton3.configure(
            text='Eliminar todos los productos \ncon el codigo seleccionado',
            value="Todos los productos",
            variable=self.obj_eliminar)
     self.radiobutton3.place(anchor="w", x=10, y=145)
    
     self.btn_cancelar= ttk.Button(self.ventana_eliminar)
     self.btn_cancelar.configure(text='Cancelar')
     self.btn_cancelar.pack(side="bottom")
     self.btn_cancelar.bind('<Button-1>', lambda _: self.salir_ventana_eliminar())

     self.btn_continuar = ttk.Button(self.ventana_eliminar)
     self.btn_continuar.configure(text='Continuar', command= self.continuar_Button)
     self.btn_continuar.pack(side="bottom")

     # Centrar la ventana emergente en la pantalla
     self.centra(self.ventana_eliminar, 350, 350)

  def salir_ventana_eliminar(self):
     self.estado_Buttons_Eliminar(True)
     self.ventana_eliminar.destroy()
     self.limpiar_Treeview()
     self.limpia_Campos()
     self.is_open_v_eliminar=None
     
  def continuar_Button(self):
     item=self.treeProductos.item(self.treeProductos.selection())
     if self.obj_eliminar.get()!='':
         if self.obj_eliminar.get()=='Producto':
            text_warning= f'Eliminar el registro del producto {item["values"][0]}, \ncorrespondiente al proveedor {item["text"]} '
         elif self.obj_eliminar.get()=='Proveedor':
            text_warning=f'Eliminar el proveedor {item["text"]} y todos \nlos registros relacionados a él '
         elif self.obj_eliminar.get()== 'Todos los productos':
            text_warning=f'Eliminar todos los registros relacionados \nal producto {item["values"][0]} '

         self.warning= self.path + r'\warning.png'

         self.ventana_confirmacion = tk.Toplevel(self.ventana_eliminar)
         self.ventana_confirmacion.configure(
               background="#ffffff",
               height=200,
               padx=10,
               pady=10,
               width=500)
         self.ventana_confirmacion.protocol("WM_DELETE_WINDOW",lambda: None)
         self.ventana_confirmacion.grab_set()
         self.ventana_confirmacion.iconbitmap(self.ico)
         self.ventana_confirmacion.resizable(False, False)
         self.ventana_confirmacion.title("Warning")

         self.img_warning = tk.PhotoImage(file=self.warning)

         self.lebel1_warning = ttk.Label(self.ventana_confirmacion)
         self.lebel1_warning.configure(image=self.img_warning)
         self.lebel1_warning.place(anchor="w", x=20, y=90)

         self.label2_warning = ttk.Label(self.ventana_confirmacion)
         self.label2_warning.configure(
               background="#ffffff",
               font="{Arial} 12 {bold}",
               text=f'Esta seguro que quiere realizar \nla siquiente acción: \n\n{text_warning}')
         self.label2_warning.place(anchor="w", x=130, y=60)

         self.btn_yes = ttk.Button(self.ventana_confirmacion)
         self.btn_yes.configure(text='Si')
         self.btn_yes.place(anchor="w", width=70, x=243, y=150)
         self.btn_yes.bind('<Button-1>', lambda _: self.btn_Yes(item) )

         self.btn_no = ttk.Button(self.ventana_confirmacion)
         self.btn_no.configure(text='No')
         self.btn_no.place(anchor="w", x=317, y=150)
         self.btn_no.bind('<Button-1>', lambda _: self.btn_No())
     
         self.centra(self.ventana_confirmacion,500,200)
     else:
        mssg.showwarning('.. Warning! ..', ' No se ha selecionado ninguna de las opciones anteriores!, por favor selecione alguna')
        self.ventana_eliminar.lift(self.win)

  def btn_Yes (self,objeto_eliminar):
     self.ventana_confirmacion.grab_release()
     self.ventana_confirmacion.destroy()
     self.salir_ventana_eliminar()
     self.elimina_Registro(objeto_eliminar)
     
  def btn_No(self):
     self.ventana_confirmacion.grab_release()
     self.ventana_confirmacion.destroy()

if __name__ == "__main__":
    app = Inventario()
    app.run()
