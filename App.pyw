from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import os
import cryptocode


class MyApp:
	database = 'Database.db'
	key = 'Alejandro'
    
	def __init__(self, parent):
		
		self.myParent = parent
		self.main_container = Frame(parent)
		self.main_container.pack(side="top", fill="both", expand=True)
		self.top_frame = Frame(self.main_container)
		self.bottom_frame = Frame(self.main_container)
		self.top_frame.pack(side="top", fill="x", expand=False)
		self.bottom_frame.pack(side="bottom", pady=20)
		
		self.titulo = ttk.Label(self.top_frame, text="Sistema de gestión de BBDD", font=("arial",20)).pack(padx=10, pady=20)
		self.top_left = Frame(self.top_frame)
		self.top_right = Frame(self.top_frame)
		self.top_left.pack(side="left", fill="x", expand=True)
		self.top_right.pack(side="right", fill="x", expand=True)
		
		self.bottom_left = Frame(self.bottom_frame)
		self.bottom_right = Frame(self.bottom_frame)
		self.bottom_left.pack(side="left", fill="both")
		self.bottom_right.pack(side="right", fill="x")
		
		# Campos

		self.id = IntVar()
		self.frameid = Frame(self.top_frame)
		self.frameid.pack(side="top", fill="x")
		self.label_id = ttk.Label(self.frameid, text="ID:", font=("arial",10)).pack(padx=10, pady=10, side='left', anchor='e')
		self.campo_id = ttk.Entry(self.frameid,textvariable=self.id).pack(padx=10, pady=10,side='right', anchor='w')
		
		self.nombre=StringVar()
		self.framename = Frame(self.top_frame)
		self.framename.pack(side="top", fill="x")
		self.label_name = ttk.Label(self.framename, text="Nombre:", font=("arial",10)).pack(padx=10, pady=10, side='left', anchor='e')
		self.campo_name = ttk.Entry(self.framename,textvariable=self.nombre).pack(padx=10, pady=10,side='right', anchor='w')
		
		self.password=StringVar()
		self.framepass = Frame(self.top_frame)
		self.framepass.pack(side="top", fill="x")
		self.label_pass = ttk.Label(self.framepass, text="Password:", font=("arial",10)).pack(padx=10, pady=10, side='left', anchor='e')
		self.campo_pass = ttk.Entry(self.framepass,textvariable=self.password, show='*').pack(padx=10, pady=10,side='right', anchor='w')
		
		self.apellido=StringVar()
		self.frame_apellido = Frame(self.top_frame)
		self.frame_apellido.pack(side="top", fill="x")
		self.label_apellido = ttk.Label(self.frame_apellido, text="Apellido:", font=("arial",10)).pack(padx=10, pady=10, side='left', anchor='e')
		self.campo_apellido = ttk.Entry(self.frame_apellido,textvariable=self.apellido).pack(padx=10, pady=10,side='right', anchor='w')
		
		self.direccion=StringVar()
		self.frame_direccion = Frame(self.top_frame)
		self.frame_direccion.pack(side="top", fill="x")
		self.label_direccion = ttk.Label(self.frame_direccion, text="Dirección:", font=("arial",10)).pack(padx=10, pady=10, side='left', anchor='e')
		self.campo_direccion = ttk.Entry(self.frame_direccion,textvariable=self.direccion).pack(padx=10, pady=10,side='right', anchor='w')

		self.frame_comentarios = Frame(self.top_frame)
		self.frame_comentarios.pack(side="top", fill="x")
		self.label_comentarios = ttk.Label(self.frame_comentarios, text="Comentarios:", font=("arial",10)).pack(pady=10, side='left', anchor='e')
		self.text_box = Text(self.frame_comentarios, height=3, width=15)
		self.scroll=Scrollbar(self.frame_comentarios, command=self.text_box.yview)
		self.scroll.pack(side='right',fill = Y )
		self.text_box.pack(side="right", anchor='w', fill='both')
		self.text_box.config(yscrollcommand=self.scroll.set)
		
		#Botones

		self.boton1=ttk.Button(self.bottom_left, text="Create", width=10, command=self.create)
		self.boton1.pack(padx=5, pady=5, side='left')
		self.boton2=ttk.Button(self.bottom_left, text="Read", width=10, command=self.read)
		self.boton2.pack(padx=5, pady=5, side='right')
		self.boton3=ttk.Button(self.bottom_right, text="Update", width=10, command=self.update)
		self.boton3.pack(padx=5, pady=5, side='left')
		self.boton4=ttk.Button(self.bottom_right, text="Delete", width=10, command=self.delete)
		self.boton4.pack(padx=5, pady=5, side='right')
		
		# BARRA MENÚ

		self.Menu=Menu(parent)
		
		self.bbddMenu=Menu(self.Menu, tearoff=0)
		self.bbddMenu.add_command(label="Conectarse", command=self.conn_bbdd)
		self.bbddMenu.add_command(label="Salir", command=salirAplicacion)
		
		self.borrarCampos=Menu(self.Menu, tearoff=0)
		self.borrarCampos.add_command(label="Borrar", command=self.borrado_campos)
		
		self.crudMenu=Menu(self.Menu, tearoff=0)
		self.crudMenu.add_command(label="Crear", command=self.create)
		self.crudMenu.add_command(label="Leer", command=self.read)
		self.crudMenu.add_command(label="Actualizar", command=self.update)
		self.crudMenu.add_command(label="Eliminar", command=self.delete)
		
		self.archivoAyuda=Menu(self.Menu, tearoff=0)
		self.archivoAyuda.add_command(label="Licencia", command=avisoLicencia)
		self.archivoAyuda.add_command(label="Acerca de", command=infoAdicional)
		
		self.Menu.add_cascade(label="BBDD", menu=self.bbddMenu)
		self.Menu.add_cascade(label="Borrar", menu=self.borrarCampos)
		self.Menu.add_cascade(label="CRUD", menu=self.crudMenu)
		self.Menu.add_cascade(label="Ayuda", menu=self.archivoAyuda)

	def conn_bbdd(self):
		global conn, cursor

		if not os.path.exists(self.database):
			conn = sqlite3.connect(self.database)
			cursor = conn.cursor()
			cursor.execute('''CREATE TABLE DATOS_USUARIOS 
				(ID INTEGER PRIMARY KEY AUTOINCREMENT,
				NOMBRE_USUARIO VARCHAR(50) UNIQUE NOT NULL CHECK (LENGTH(NOMBRE_USUARIO)>1),
				PASSWORD VARCHAR(50) NOT NULL CHECK (LENGTH(NOMBRE_USUARIO)>1),
				APELLIDO VARCHAR(10) NOT NULL CHECK (LENGTH(NOMBRE_USUARIO)>1),
				DIRECCION VARCHAR(50) NOT NULL CHECK (LENGTH(NOMBRE_USUARIO)>1),
				COMENTARIOS VARCHAR(100) NOT NULL)''')
		else:
			conn = sqlite3.connect(self.database)
			cursor = conn.cursor()

	def borrado_campos(self):
		self.id.set(0)
		self.nombre.set('')
		self.password.set('')
		self.apellido.set('')
		self.direccion.set('')
		self.text_box.delete('1.0',"end")

	def encriptar(self):
		return cryptocode.encrypt(self.password.get(),self.key)

	def desencriptar(self,password):
		return cryptocode.decrypt(password, self.key)
	
	def create(self):
		try:
			password = self.encriptar()
			cursor.execute(f'INSERT INTO DATOS_USUARIOS VALUES (NULL,"{self.nombre.get()}","{password}","{self.apellido.get()}","{self.direccion.get()}","{self.text_box.get(1.0, "end-1c")}")')
			conn.commit()
			self.borrado_campos()
			okcheck()
		except NameError:
				error_conn()
		except:
			mensaje_error()

	def read(self):
		try:
			id = self.id.get()
			cursor.execute(f'SELECT * FROM DATOS_USUARIOS WHERE ID={id}')
			persona = cursor.fetchone()
			if persona == None:
				messagebox.showwarning("Error", "El id ingresado no le pertenece a ningún usuario en la base de datos.")
			else:
				self.nombre.set(persona[1])
				password = self.desencriptar(str(persona[2]))
				self.password.set(password)
				self.apellido.set(persona[3])
				self.direccion.set(persona[4])
				self.text_box.delete('1.0',"end")
				self.text_box.insert('1.0', persona[5])
		except NameError:
			error_conn()

	def update(self):
		try:
			id = self.id.get()
			cursor.execute(f'SELECT * FROM DATOS_USUARIOS WHERE ID={id}')
			persona = cursor.fetchone()
			if persona == None:
				messagebox.showwarning("Error", "El id ingresado no le pertenece a ningún usuario en la base de datos.")
			else:
				password = self.encriptar()
				cursor.execute(f'UPDATE DATOS_USUARIOS SET NOMBRE_USUARIO="{self.nombre.get()}", PASSWORD="{password}", APELLIDO="{self.apellido.get()}",DIRECCION="{self.direccion.get()}",COMENTARIOS={self.text_box.get(1.0, "end-1c")} WHERE ID={self.id.get()}')
				conn.commit()
				self.borrado_campos()
				okcheck()
		except NameError:
			error_conn()


	def delete(self):
		try:
			id = self.id.get()
			cursor.execute(f'SELECT * FROM DATOS_USUARIOS WHERE ID={id}')
			persona = cursor.fetchone()
			if persona == None:
				messagebox.showwarning("Error", "El id ingresado no le pertenece a ningún usuario en la base de datos.")
			else:
				valor=messagebox.askquestion("Eliminar", f"¿Está seguro de que desea eliminar a {persona[1]}?")
				if valor=="yes":
					cursor.execute(f'DELETE FROM DATOS_USUARIOS WHERE ID={id}')
					conn.commit()
					self.borrado_campos()
					okcheck()
		except NameError:
			error_conn()
		except:
			mensaje_error()

def darkstyle(root):
   
    style = ttk.Style(root)
    root.tk.call('source', 'azure dark/azure dark.tcl')
    style.theme_use('azure')
    style.configure("Accentttk.Button", foreground='white')
    style.configure("Togglettk.Button", foreground='white')
    return style

def infoAdicional():
	messagebox.showinfo("Procesador de Juan", "Procesador de textos versión 2018")

def okcheck():
	messagebox.showinfo("Todo correcto", "Todo salió como se esperaba!")	

def avisoLicencia():
	messagebox.showwarning("Licencia", "Producto bajo licencia GNU")

def error_conn():
	messagebox.showwarning("Error", "No puedes realizar una operación sin antes conectarte a la base de datos")

def mensaje_error():
	messagebox.showwarning("Error", "El usuario no fue cargado por algún dato inválido, por favor corrijalo inténtelo nuevamente")

def salirAplicacion():
	valor=messagebox.askquestion("Salir", "¿Desea salir de la aplicación?")
	if valor=="yes":
		try:
			cursor.close()
			conn.close()
		except:
			pass
		finally:
			root.destroy()

def main():
	global root, myapp

	root = Tk()
	myapp = MyApp(root)
	root.config(width=440, height=530, padx=5, pady=5,menu=myapp.Menu)
	root.title("Sistema de gestión de BBDD")
	root.iconbitmap("icon.ico")
	root.resizable(0,0)
	img = PhotoImage(file="Fondo.png")
	style = darkstyle(root)
	root.mainloop()

if __name__ =='__main__':
	main()