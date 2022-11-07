from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import os
import cryptocode


class MyApp:

	
	# Change this vars before start
	#-----------------------------------------------------------------
	database = 'Database.db'
	key = 'Example key'
        #-----------------------------------------------------------------

	def __init__(self, parent):
		
		self.myParent = parent
		self.main_container = Frame(parent)
		self.main_container.pack(side="top", fill="both", expand=True)
		self.top_frame = Frame(self.main_container)
		self.bottom_frame = Frame(self.main_container)
		self.top_frame.pack(side="top", fill="x", expand=False)
		self.bottom_frame.pack(side="bottom", pady=20)
		
		self.title = ttk.Label(self.top_frame, text="BBDD manager", font=("arial",20)).pack(padx=10, pady=20)
		self.top_left = Frame(self.top_frame)
		self.top_right = Frame(self.top_frame)
		self.top_left.pack(side="left", fill="x", expand=True)
		self.top_right.pack(side="right", fill="x", expand=True)
		
		self.bottom_left = Frame(self.bottom_frame)
		self.bottom_right = Frame(self.bottom_frame)
		self.bottom_left.pack(side="left", fill="both")
		self.bottom_right.pack(side="right", fill="x")
		
		# Fields

		self.id = IntVar()
		self.id_frame = Frame(self.top_frame)
		self.id_frame.pack(side="top", fill="x")
		self.id_label = ttk.Label(self.id_frame, text="ID:", font=("arial",10)).pack(padx=10, pady=10, side='left', anchor='e')
		self.id_field = ttk.Entry(self.id_frame,textvariable=self.id).pack(padx=10, pady=10,side='right', anchor='w')
		
		self.name=StringVar()
		self.frame_name = Frame(self.top_frame)
		self.frame_name.pack(side="top", fill="x")
		self.label_name = ttk.Label(self.frame_name, text="Name:", font=("arial",10)).pack(padx=10, pady=10, side='left', anchor='e')
		self.field_name = ttk.Entry(self.frame_name,textvariable=self.name).pack(padx=10, pady=10,side='right', anchor='w')
		
		self.password=StringVar()
		self.password_frame = Frame(self.top_frame)
		self.password_frame.pack(side="top", fill="x")
		self.password_label = ttk.Label(self.password_frame, text="Password:", font=("arial",10)).pack(padx=10, pady=10, side='left', anchor='e')
		self.password_field = ttk.Entry(self.password_frame,textvariable=self.password, show='*').pack(padx=10, pady=10,side='right', anchor='w')
		
		self.surname=StringVar()
		self.surname_frame = Frame(self.top_frame)
		self.surname_frame.pack(side="top", fill="x")
		self.surname_label = ttk.Label(self.surname_frame, text="Surname:", font=("arial",10)).pack(padx=10, pady=10, side='left', anchor='e')
		self.surname_field = ttk.Entry(self.surname_frame,textvariable=self.surname).pack(padx=10, pady=10,side='right', anchor='w')
		
		self.address=StringVar()
		self.address_frame = Frame(self.top_frame)
		self.address_frame.pack(side="top", fill="x")
		self.address_label = ttk.Label(self.address_frame, text="Address:", font=("arial",10)).pack(padx=10, pady=10, side='left', anchor='e')
		self.address_field = ttk.Entry(self.address_frame,textvariable=self.address).pack(padx=10, pady=10,side='right', anchor='w')

		self.comments_frame = Frame(self.top_frame)
		self.comments_frame.pack(side="top", fill="x")
		self.comments_label = ttk.Label(self.comments_frame, text="Comments:", font=("arial",10)).pack(pady=10, side='left', anchor='e')
		self.text_box = Text(self.comments_frame, height=3, width=15)
		self.scroll=Scrollbar(self.comments_frame, command=self.text_box.yview)
		self.scroll.pack(side='right',fill = Y )
		self.text_box.pack(side="right", anchor='w', fill='both')
		self.text_box.config(yscrollcommand=self.scroll.set)
		
		# Buttons

		self.button1=ttk.Button(self.bottom_left, text="Create", width=10, command=self.create)
		self.button1.pack(padx=5, pady=5, side='left')
		self.button2=ttk.Button(self.bottom_left, text="Read", width=10, command=self.read)
		self.button2.pack(padx=5, pady=5, side='right')
		self.button3=ttk.Button(self.bottom_right, text="Update", width=10, command=self.update)
		self.button3.pack(padx=5, pady=5, side='left')
		self.button4=ttk.Button(self.bottom_right, text="Delete", width=10, command=self.delete)
		self.button4.pack(padx=5, pady=5, side='right')
		
		# Menú bar

		self.menu=Menu(parent)
		
		self.bbdd_menu=Menu(self.menu, tearoff=0)
		self.bbdd_menu.add_command(label="Connect", command=self.bbdd_conn)
		self.bbdd_menu.add_command(label="Exit", command=exit_app)
		
		self.erase_fields=Menu(self.menu, tearoff=0)
		self.erase_fields.add_command(label="Clean", command=self.fields_erase)
		
		self.crudMenu=Menu(self.menu, tearoff=0)
		self.crudMenu.add_command(label="Create", command=self.create)
		self.crudMenu.add_command(label="Read", command=self.read)
		self.crudMenu.add_command(label="Update", command=self.update)
		self.crudMenu.add_command(label="Delete", command=self.delete)
		
		self.help=Menu(self.menu, tearoff=0)
		self.help.add_command(label="License", command=license_warning)
		self.help.add_command(label="About", command=additional_info)
		
		self.menu.add_cascade(label="BBDD", menu=self.bbdd_menu)
		self.menu.add_cascade(label="Clean", menu=self.erase_fields)
		self.menu.add_cascade(label="CRUD", menu=self.crudMenu)
		self.menu.add_cascade(label="Help", menu=self.help)

	def bbdd_conn(self):
		global conn, cursor

		if not os.path.exists(self.database):
			conn = sqlite3.connect(self.database)
			cursor = conn.cursor()
			cursor.execute('''CREATE TABLE USERS_DATA 
				(ID INTEGER PRIMARY KEY AUTOINCREMENT,
				USERNAME VARCHAR(50) UNIQUE NOT NULL CHECK (LENGTH(USERNAME)>1),
				PASSWORD VARCHAR(50) NOT NULL CHECK (LENGTH(PASSWORD)>1),
				SURNAME VARCHAR(10) NOT NULL CHECK (LENGTH(SURNAME)>1),
				ADDRESS VARCHAR(50) NOT NULL CHECK (LENGTH(ADDRESS)>1),
				COMMENTS VARCHAR(100) NOT NULL)''')
		else:
			conn = sqlite3.connect(self.database)
			cursor = conn.cursor()

	def fields_erase(self):
		self.id.set(0)
		self.name.set('')
		self.password.set('')
		self.surname.set('')
		self.address.set('')
		self.text_box.delete('1.0',"end")

	def encrypt(self):
		return cryptocode.encrypt(self.password.get(),self.key)

	def decrypt(self,password):
		return cryptocode.decrypt(password, self.key)
	
	def create(self):
		try:
			password = self.encrypt()
			cursor.execute(f'INSERT INTO USERS_DATA VALUES (NULL,"{self.name.get()}","{password}","{self.surname.get()}","{self.address.get()}","{self.text_box.get(1.0, "end-1c")}")')
			conn.commit()
			self.fields_erase()
			ok_check()
		except NameError:
				conn_error()
		except:
			error_msg()

	def read(self):
		try:
			id = self.id.get()
			cursor.execute(f'SELECT * FROM USERS_DATA WHERE ID={id}')
			person = cursor.fetchone()
			if person == None:
				messagebox.showwarning("Error", "The entered id does not belong to any database user.")
			else:
				self.name.set(person[1])
				password = self.decrypt(str(person[2]))
				self.password.set(password)
				self.surname.set(person[3])
				self.address.set(person[4])
				self.text_box.delete('1.0',"end")
				self.text_box.insert('1.0', person[5])
		except NameError:
			conn_error()

	def update(self):
		try:
			id = self.id.get()
			cursor.execute(f'SELECT * FROM USERS_DATA WHERE ID={id}')
			person = cursor.fetchone()
			if person == None:
				messagebox.showwarning("Error", "The entered id does not belong to any database user.")
			else:
				password = self.encrypt()
				cursor.execute(f'UPDATE USERS_DATA SET USERNAME="{self.name.get()}", PASSWORD="{password}", SURNAME="{self.surname.get()}",ADDRESS="{self.address.get()}",COMMENTS="{self.text_box.get(1.0, "end-1c")}" WHERE ID={id}')
				conn.commit()
				self.fields_erase()
				ok_check()
		except NameError:
			conn_error()

	def delete(self):
		try:
			id = self.id.get()
			cursor.execute(f'SELECT * FROM USERS_DATA WHERE ID={id}')
			person = cursor.fetchone()
			if person == None:
				messagebox.showwarning("Error", "The entered id does not belong to any database user.")
			else:
				valor=messagebox.askquestion("Delete", f"¿Are you sure you want to delete {person[1]}?")
				if valor=="yes":
					cursor.execute(f'DELETE FROM USERS_DATA WHERE ID={id}')
					conn.commit()
					self.fields_erase()
					ok_check()
		except NameError:
			conn_error()
		except:
			error_msg()

def dark_theme(root):
    style = ttk.Style(root)
    root.tk.call('source', 'azure dark/azure dark.tcl')
    style.theme_use('azure')
    style.configure("Accentttk.Button", foreground='white')
    style.configure("Togglettk.Button", foreground='white')
    return style

def additional_info():
	messagebox.showinfo("Example info", "Just to complete a bit the program")

def ok_check():
	messagebox.showinfo("Everything correct", "Everything went correct!")	

def license_warning():
	messagebox.showwarning("License", "Product under x license...")

def conn_error():
	messagebox.showwarning("Error", "You cannot perform an operation without first connecting to the database")

def error_msg():
	messagebox.showwarning("Error", "The user was not created due to some invalid data, please correct it and try again")

def exit_app():
	valor=messagebox.askquestion("Exit", "¿Do you want to exit the app?")
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
	root.config(width=440, height=530, padx=5, pady=5,menu=myapp.menu)
	root.title("BBDD manager")
	root.iconbitmap("icon.ico")
	root.resizable(0,0)
	img = PhotoImage(file="bg.png")
	style = dark_theme(root)
	root.mainloop()

if __name__ =='__main__':
	main()
