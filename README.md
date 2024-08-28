# Alejas² and Migue Stock Wizard

***"A project full of frustrations and joys, but above all, lessons"*** now for this project ;)

**By Fotocopiadora Alejas² and Migue**

(logo?)

![Logo](loguito.png)

## Planning
 

## Development
  (solution to the problem posed, solution explanation, class diagrams with code and class-by-class explanation)

  El problema se abordó diseñando una aplicación de gestión de inventario en Python que se enfoca en la administración eficiente de productos y proveedores. Para plantear la solución, se creó una estructura  donde una clase principal gestiona las operaciones fundamentales del sistema, como el manejo de datos y la interacción con el usuario. Se implementaron métodos para validar información, realizar operaciones CRUD (crear, leer, actualizar, eliminar) y manejar la interfaz gráfica. Además, se incluyeron características adicionales como la carga masiva de registros, la persistencia de datos mediante una base de datos y la generación de reportes. Este enfoque permite una gestión integral del inventario, garantizando la integridad de los datos y una experiencia de usuario fluida.


### Structure

Inventario: Esta clase representa la aplicación de gestión de inventario. A través de esta clase, se realiza la conexión con la base de datos, se gestionan los productos y proveedores, y se maneja la interfaz de usuario.

#### ```__Init__```

```python
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

```

En el constructor (__init__) se configura la interfaz gráfica usando tkinter. Se define la ventana principal con tamaño, ícono, y título. Dentro de esta ventana, se crea un contenedor (LabelFrame) con un Notebook para gestionar pestañas.

La primera pestaña (frm1) incluye campos de entrada y etiquetas para capturar información del proveedor y del producto, como ID/Nit, nombre, precios, y fechas. Se añade un Treeview para mostrar los datos en formato tabular y una barra de desplazamiento vertical para manejar grandes volúmenes de datos.

También se agregan botones para buscar, guardar, editar, eliminar y cancelar operaciones. Los widgets se colocan usando el método place() y se organizan en dos frames: uno para los datos y otro para los botones.

Finalmente, se asigna la ventana principal al atributo mainwindow, preparándola para su visualización.

#### ```Databuild base and run```

```python
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
```

Data base crea dos tablas en la base de datos si no existen ya. La primera tabla, Productos, almacena información sobre productos con campos como ID/Nit, código, nombre, unidad, cantidad, precio y fecha de vencimiento, donde la combinación de código e ID/Nit es la clave primaria. La segunda tabla, Proveedores, guarda datos de proveedores, incluyendo ID, nombre y fecha de compra, con el ID como clave primaria.

Run primero llama a database_build() para asegurarse de que las tablas necesarias están presentes en la base de datos. Luego, inicia el bucle principal de la interfaz gráfica con mainwindow.mainloop(), lo que permite que la ventana se mantenga abierta y responda a las interacciones del usuario.

####  ''' ......... Métodos utilitarios del sistema .............'''

```python
  #Rutina de centrado de pantalla
  def centra(self,win,ancho,alto): 
      """ centra las ventanas en la pantalla """ 
      x = win.winfo_screenwidth() // 2 - ancho // 2 
      y = win.winfo_screenheight() // 2 - alto // 2 
      win.geometry(f'{ancho}x{alto}+{x}+{y}') 
      win.deiconify() # Se usa para restaurar la ventana
```

Centra la ventana win en la pantalla. Calcula las coordenadas (x, y) para posicionar la ventana en el centro del monitor, basándose en el tamaño de la ventana (ancho y alto). Luego, ajusta la geometría de la ventana para que esté centrada y restaurar su visibilidad con win.deiconify(), en caso de que estuviera minimizada o escondida.

```python
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
```
Estas funciones realizan validaciones para asegurar la integridad y el formato correcto de los datos ingresados en el formulario. Cada función se enfoca en un campo específico y verifica condiciones como la longitud máxima de texto, la presencia de caracteres no permitidos, y el formato adecuado para fechas y números. Al implementar estas validaciones, el sistema ayuda a prevenir errores de entrada que podrían afectar el funcionamiento del programa o la calidad de los datos almacenados. Además, proporciona retroalimentación inmediata al usuario para corregir cualquier entrada incorrecta antes de que se procese.

* valida_Id_Nit: Valida que el campo idNit no contenga más de 15 caracteres y no incluya espacios. Si se ingresan espacios, se eliminan y se muestra un mensaje de error. Si la longitud excede los 15 caracteres, se trunca y se muestra un mensaje de error.

* valida_Nombre_Proveedor: Valida que el campo nombre Proveedor no tenga más de 25 caracteres. Si se excede este límite, se trunca el texto y se muestra un mensaje de error.

* validaFechaC: Valida la fecha en el campo fechaCompra. Si la fecha es inválida o está vacía, se muestra un mensaje de error y se restablece el campo a su estado predeterminado. Si está vacío, se coloca el formato de fecha por defecto.

* escribirFechaC: Formatea el texto ingresado en el campo fechaCompra como una fecha (dd/mm/yyyy). Inserta las barras / en las posiciones correctas y verifica que la longitud no exceda los 10 caracteres. Si la fecha es inválida, se muestra un mensaje de error y se limpia el campo.

* borrarFechaC: Limpia el campo fechaCompra si contiene el texto predeterminado dd/mm/yyyy y restaura el estado del campo para permitir la edición.

* valida_Codigo: Valida que el campo codigo no tenga más de 15 caracteres y no incluya espacios. Si se ingresan espacios, se eliminan y se muestra un mensaje de error. Si la longitud excede los 15 caracteres, se trunca y se muestra un mensaje de error.

* valida_Nombre_Producto: Valida que el campo nombreProducto no tenga más de 50 caracteres. Si se excede este límite, se trunca el texto y se muestra un mensaje de error.

* valida_Unidad: Valida que el campo unidad no tenga más de 10 caracteres. Si se excede este límite, se trunca el texto y se muestra un mensaje de error.

* valida_Cantidad: Valida que el campo cantidad no tenga más de 6 caracteres y que su valor sea un número válido. Si se excede el límite o el valor no es un número, se muestra un mensaje de error y se limpia el campo.

* valida_Precio_Compra: Valida que el campo precioCompra no tenga más de 9 caracteres y que el valor ingresado sea un número válido. Si se excede el límite o el valor no es un número, se muestra un mensaje de error y se limpia el campo.

* validaFechaV: Valida la fecha en el campo fechaVencimiento. Si la fecha es inválida o está vacía, se muestra un mensaje de error y se restablece el campo a su estado predeterminado. Si está vacío, se coloca el formato de fecha por defecto.

* escribirFechaV: Formatea el texto ingresado en el campo fechaVencimiento como una fecha (dd/mm/yyyy). Inserta las barras / en las posiciones correctas y verifica que la longitud no exceda los 10 caracteres. Si la fecha es inválida, se muestra un mensaje de error y se limpia el campo.

* borrarFechaV: Limpia el campo fechaVencimiento si contiene el texto predeterminado dd/mm/yyyy y restaura el estado del campo para permitir la edición.

* validar_ID: Verifica si el idNit ingresado ya existe en la base de datos de proveedores. Retorna True si existe, de lo contrario False.

* validar_Cod:Verifica si el codigo ingresado ya existe en la base de datos de productos. Retorna True si existe, de lo contrario False.

```python
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
```
Estas rutinas se utilizan para gestionar la presentación y actualización de datos en la interfaz de usuario. La función limpia_Campos se encarga de vaciar todos los campos de entrada en el formulario, lo cual es crucial cuando se termina de procesar o guardar datos, asegurando que no queden valores antiguos que puedan causar confusión o errores. La función limpiar_Treeview elimina todas las entradas visibles en la tabla de productos, permitiendo que la interfaz muestre solo los datos actuales y relevantes. La función cargar_Datos_Treeview se encarga de insertar los datos actualizados en la tabla, proporcionando al usuario la información más reciente y correcta. Estas acciones garantizan que la interfaz de usuario esté limpia y que los datos sean siempre precisos y actualizados.

* limpia_Campos: Limpia todos los campos de entrada en la interfaz de usuario(Restablece el campo idNit y codigo a su estado editable y borra su contenido. Limpia los campos nombreProveedor, fechaCompra, nombreProducto, unidad, cantidad, precioCompra, y fechaVencimiento).

* limpiar_Treeview: Elimina todas las filas del widget Treeview (una tabla de datos en la interfaz gráfica). Recorre todas las filas actuales y las elimina una por una.

* cargar_Datos_Treeview: Carga datos en el widget Treeview desde una lista de filas (db_rows): Primero, procesa los datos para manejar valores nulos mediante change_Nulls_Fetchall. Luego, inserta cada fila de datos en el Treeview, utilizando el primer valor como texto (para la clave de cada fila) y el resto de los valores para las columnas asociadas.

```python
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

```

Esta sección del código maneja la interacción entre una aplicación de gestión de inventarios y su base de datos. Su propósito es realizar operaciones fundamentales como la búsqueda, inserción, actualización y eliminación de registros de proveedores y productos. Permite al usuario consultar información existente, agregar nuevos datos, actualizar registros existentes y eliminar aquellos que ya no sean necesarios. Cada función está diseñada para ejecutar una tarea específica, como insertar un nuevo proveedor o producto en la base de datos, o actualizar detalles de un registro ya existente.

Además, el código gestiona cómo se presentan y actualizan estos datos en la interfaz de usuario, asegurando que las operaciones se realicen de manera eficiente y correcta. Por ejemplo, maneja casos donde los campos pueden estar vacíos o contener valores nulos, y asegura que el usuario confirme acciones importantes, como la eliminación de registros, para evitar errores o pérdidas de datos accidentales. En resumen, esta sección organiza y controla cómo se manejan los datos en la base de datos y cómo estos datos se reflejan en la interfaz de usuario de la aplicación.

* run_Query: Ejecuta una consulta SQL con parámetros opcionales en la base de datos y retorna el resultado.

* accion_Buscar: Ejecuta una consulta SELECT en una tabla dada, basándose en una condición y parámetros opcionales.

* accion_Eliminar: Elimina registros de una tabla específica basándose en una condición y valores dados.

* insertar_Proveedor: Inserta un nuevo proveedor en la tabla Proveedores. Convierte cadenas vacías en valores nulos antes de la inserción.

* insertar_Producto: Inserta un nuevo producto en la tabla Productos. Convierte cadenas vacías en valores nulos antes de la inserción.

* actualizar_Proveedor: Actualiza la información del proveedor en la tabla Proveedores si hay cambios.

* actualizar_Producto: Actualiza la información del producto en la tabla Productos si hay cambios.

* cargar_Proveedor: Carga y muestra los datos del proveedor en los campos de entrada correspondientes.

* cargar_Producto: Carga y muestra los datos del producto en los campos de entrada correspondientes.

* change_Nulls_Fetchone: Reemplaza None en una lista por cadenas vacías y convierte los elementos a cadenas.

* change_Nulls_Fetchall: Reemplaza None en listas anidadas por cadenas vacías y convierte todos los elementos a cadenas.

* change_Emptystring_To_Null: Reemplaza cadenas vacías en una lista por None.

* search_Button: Realiza una búsqueda basada en el ID o código ingresado. Muestra mensajes de error si no se ingresa un valor o si los valores no son válidos.

* cargar_Datos_Buscados: Limpia y carga los datos de búsqueda en el Treeview.

* cancel_Button_Main_Win: Cancela la edición y restaura los campos a su estado inicial. También gestiona el estado de los botones.

* record_Button: Adiciona o actualiza un registro en la base de datos según el modo de edición actual.

* adiciona_Registro: Adiciona un producto a la base de datos si las validaciones son correctas y muestra mensajes de confirmación.

* carga_Datos: Carga los datos del producto seleccionado en los campos de entrada y activa el modo de edición.

* estado_Buttons_Editar: Habilita o deshabilita los botones de búsqueda, edición, y eliminación según el estado dado.

* actualizar_datos: Actualiza los datos del proveedor y del producto si hay cambios y muestra mensajes de confirmación.

* eliminar_Button: Abre la ventana de confirmación para eliminar un registro si se selecciona uno en el Treeview.

* estado_Buttons_Eliminar: Habilita o deshabilita los botones de búsqueda, guardar, editar y eliminar según el estado dado.

* elimina_Registro: Elimina un registro de la base de datos según el tipo de eliminación seleccionada.

* abrir_Ventana_Eliminar: Crea y muestra una ventana de confirmación para la eliminación de registros.

* salir_ventana_eliminar: Cierra la ventana de eliminación y restaura el estado de los botones.

* continuar_Button: Muestra una ventana de confirmación para la acción de eliminación seleccionada.

* btn_Yes: Confirma la eliminación del registro seleccionado y realiza la acción de eliminación.

* btn_No: Cancela la acción de eliminación y cierra la ventana de confirmación.


#### If__name__ = "__main__":

```python
if __name__ == "__main__":
    app = Inventario()
    app.run()
```
Ejecutador

## Complete code

```python
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
```


## How to install and use the program

El código debe tener la estructura en forma de paquete.
Se debe incluir los requerimientos para crear un entorno virtual.
Opcional:
GUI, Docker, Manejod e Hilos.


En primer lugar, para poder obtener la base de datos, se debe comprender que esta creada en un formato SQL por lo que se recomienda instalar SQLite Viewer y sqlite3, que permitiran visualizar y poder programar de manera adecuada.

SQL es útil en la Programación Orientada a Objetos (POO) porque permite guardar y recuperar objetos de forma sencilla en bases de datos, manteniendo su estado entre sesiones. Además, facilita la búsqueda de datos relacionados, aprovechando la estructura relacional de las tablas
