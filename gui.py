import tkinter
from tkinter import Label, Entry, Button, StringVar, Listbox, ttk
import tkinter as tk
from tkinter.font import Font


# Colors
BG_COLOR = '#353b48'
BTN_COLOR = '#2f3542'
TEXT_COLOR = '#ffffff'
ERROR_BACKGROUND = '#e74c3c'
ERROR_MSG = '#d50000'
SUCCESS_BACKGROUND = '#689F38'
SUCESS_MSG = '#1B5E20'

class LoginGUI:
	def __init__(self, database):
		# Database
		self.db = database

		# Background Color
		self.window = tkinter.Tk()
		self.window['background'] = BG_COLOR
		
		# Password Label
		self.password_label = Label(self.window, text='Login/Register', bg=BG_COLOR, fg=TEXT_COLOR, font=Font(family='Helvetica', size=16)).grid(row=0, columnspan=4, padx=10, pady=10)
		
		# Text Entry
		self.master_user = StringVar()
		self.master_password = StringVar()
		self.master_user_label = Label(self.window, text='Username', bg=BG_COLOR, fg=TEXT_COLOR, font=Font(family='Helvetica', size=16)).grid(row=1, column=0, columnspan=2, padx=10, pady=10)
		self.master_password_label = Label(self.window, text='Password', bg=BG_COLOR, fg=TEXT_COLOR, font=Font(family='Helvetica', size=16)).grid(row=2, column=0, columnspan=2, padx=10, pady=10)
		self.master_user_entry = Entry(self.window, textvariable=self.master_user, font=Font(family='Helvetica', size=16))
		self.master_password_entry = Entry(self.window, textvariable=self.master_password, font=Font(family='Helvetica', size=16))
		self.master_user_entry.grid(row=1, column=2, columnspan=2, padx=10, pady=10)
		self.master_password_entry.grid(row=2, column=2, columnspan=2, padx=10, pady=10)
		
		# Buttons
		self.login_btn = Button(self.window, text="Login", bg=BTN_COLOR, fg=TEXT_COLOR, font=Font(family='Helvetica', size=16), highlightthickness=0, bd=0, command=self.login)
		self.register_btn = Button(self.window, text='Register', bg=BTN_COLOR, fg=TEXT_COLOR, font=Font(family='Helvetica', size=16), highlightthickness=0, bd=0, command=self.register)
		
		# Pack The Buttons
		self.login_btn.grid(row=3, column=0, columnspan=2, sticky='ew', padx=10, pady=10)
		self.register_btn.grid(row=3, column=2, columnspan=2, stick='ew', padx=10, pady=10)
		
		# Main Loop
		self.window.mainloop()

	def register(self):
		# Gets the Input fields
		master_usr = self.master_user.get()
		master_pass = self.master_password.get()

		# If both the fields are filled out
		if len(master_usr) > 0 and len(master_pass) > 0:
			response = self.db.createMasterUser(master_usr, master_pass)
			if not(response): # If Account already exists
				self.displayMessage("Account already exists", False)
			else: # If account is successfully created
				self.displayMessage("Account Created", True)
		else: # If any fields are left blank
			self.displayMessage("Fill all fields", False)

	def login(self):
		master_usr = self.master_user.get()
		master_pass = self.master_password.get()

		# If both the fields are filled out
		if len(master_usr) > 0 and len(master_pass) > 0:
			response = self.db.validateLogin(master_usr, master_pass)
			if not(response):
				self.displayMessage("Wrong Username or Password", False)
			else:
				self.window.destroy()
				newGUI = MainGUI(self.db, master_usr)
		else:
			self.displayMessage("Fill all fields", False)


	def displayMessage(self, msg, is_success):
		# Removes any message which were created there before
		self.removeMessage()

		# Sets the color scheme based on if the message is a success message or error message
		color_scheme = (SUCCESS_BACKGROUND, SUCESS_MSG) if is_success else (ERROR_BACKGROUND, ERROR_MSG)

		# Changes Position of Buttons to show message
		self.login_btn.grid(row=4, column=0, sticky='ew', padx=10, pady=10)
		self.register_btn.grid(row=4, column=1, stick='ew', padx=10, pady=10)

		# Message
		self.msg = Label(self.window, text=msg, font=Font(family='Helvetica', size=10), bg=color_scheme[0], fg=color_scheme[1])
		self.msg.grid(row=3, columnspan=2, padx=10, pady=10)

	def removeMessage(self):
		try: # If the error msg has been created yet
			self.msg.grid_forget()
		except:
			pass

class MainGUI:
	def __init__(self, db, user):
		# Initialize the database again
		self.db = db

		# Get user
		self.user = user
		self.user_data = self.db.getUserPasswords(self.user)
		self.count = len(self.user_data)
		self.iid = len(self.user_data)
		self.list_maintain = []

		# Make Window
		self.window = tkinter.Tk()
		self.window['background'] = BG_COLOR

		# Password Manager Label
		self.password_manage_label = Label(self.window, text='Password Manager', bg=BG_COLOR, fg=TEXT_COLOR, font=Font(family='Helvetica', size=16)).grid(row=0, column=0, columnspan=4, padx=10, pady=10)


		# List of Passwords
		self.password_list = ttk.Treeview(self.window, height=10, selectmode='browse')
		self.password_list['columns'] = ('Username', 'Password')
		self.password_list.heading("#0", text='Account')
		self.password_list.heading("#1", text='Username')
		self.password_list.heading("#2", text='Password')
		self.password_list.column('#0', stretch=tk.YES)
		self.password_list.column('#1', stretch=tk.YES)
		self.password_list.column('#2', stretch=tk.YES)
		self.password_list.grid(row=1, column=0, columnspan=4, padx=10, pady=10)
		for data in self.user_data:
			self.password_list.insert('', 'end', iid=self.user_data.index(data)+1, text=str(self.user_data.index(data)+1), values=(data[0], data[1]))
			self.list_maintain.append((data[0], data[1]))

		# Username And Password
		self.username_label = Label(self.window, text='Username', bg=BG_COLOR, fg=TEXT_COLOR, font=Font(family='Helvetica', size=16)).grid(row=2, column=0, padx=10, pady=10)
		self.password_label = Label(self.window, text='Password', bg=BG_COLOR, fg=TEXT_COLOR, font=Font(family='Helvetica', size=16)).grid(row=3, column=0, padx=10, pady=10)

		# Add Password
		self.account_user = StringVar()
		self.account_password = StringVar()
		self.account_user_entry = Entry(self.window, textvariable=self.account_user, font=Font(family='Helvetica', size=16))
		self.account_password_entry = Entry(self.window, textvariable=self.account_password, font=Font(family='Helvetica', size=16))
		self.account_user_entry.grid(row=2, column=1, columnspan=4, padx=10, pady=10)
		self.account_password_entry.grid(row=3, column=1, columnspan=4, padx=10, pady=10)

		# Button
		self.add_button = Button(self.window, text="Add Password", bg=BTN_COLOR, fg=TEXT_COLOR, font=Font(family='Helvetica', size=16), highlightthickness=0, bd=0, width=45, command=self.addPassword)
		self.add_button.grid(row=4, column=0, columnspan=5, padx=10, pady=10)

		# Remove Button
		self.remove_button = Button(self.window, text='Remove Password', bg=BTN_COLOR, fg=TEXT_COLOR, font=Font(family='Helvetica', size=16), highlightthickness=0, bd=0, width=45, command=self.deletePassword)
		self.remove_button.grid(row=5, column=0, columnspan=5, padx=10, pady=10)


	def addPassword(self):
		username = self.account_user.get()
		password = self.account_password.get()
		if len(username) > 0 and len(password) > 0:
			self.count += 1
			self.iid += 1
			self.db.addUserPassword(username, password, self.user)
			self.password_list.insert('', 'end', iid=self.iid, text=str(self.count), values=(username, password))
			self.list_maintain.append((username, password))

	def deletePassword(self):
		row_id = self.password_list.focus()
		item = self.list_maintain[int(row_id)-1]
		self.db.deleteUserPassword(item[0], item[1], self.user)
		self.password_list.delete(row_id)



