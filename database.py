import sqlite3

class Database:
	def __init__(self, name, encrypter):
		self.encryption = encrypter
		self.conn = sqlite3.connect(name)
		self.c = self.conn.cursor()
		self.c.execute('''
			CREATE TABLE IF NOT EXISTS Accounts(account text, password text, masterusername text);
			''')
		self.c.execute("""
			CREATE TABLE  IF NOT EXISTS MasterAccounts(username text, password text);
			""")


	def createMasterUser(self, username, password):
		account = self.getMasterUser(username)
		if account != None:
			return False
		else:
			new_password = self.encryption.encrypt(password)
			self.c.execute('INSERT INTO MasterAccounts VALUES (?, ?)', (username, new_password))
			self.conn.commit()
			return True


	def validateLogin(self, username, password):
		account = self.getMasterUser(username)
		if account != None:
			decrypted_password = self.encryption.decrypt(account[1])
			if password == decrypted_password:
				return True
			else:
				return False
		else:
			return False

	def getMasterUser(self, username):
		checker = self.c.execute('SELECT * FROM MasterAccounts WHERE username=?', (username, ))
		return checker.fetchone()


	def getUserPasswords(self, masterusername):
		user_data = self.c.execute('SELECT * FROM Accounts WHERE masterusername=?', (masterusername, ))
		new_list = []
		for data in user_data.fetchall():
			decrypted_password = self.encryption.decrypt(data[1])
			new_list.append((data[0], decrypted_password))
		return new_list


	def addUserPassword(self, username, password, masterusername):
		encrypted_password = self.encryption.encrypt(password)
		self.c.execute("INSERT INTO Accounts VALUES (?, ?, ?)", (username, encrypted_password, masterusername))
		self.conn.commit()


	def deleteUserPassword(self, username, password, masterusername):
		encrypted_password = self.encryption.encrypt(password)
		self.c.execute("DELETE FROM Accounts WHERE account = ? AND password = ? AND masterusername = ?", (username, encrypted_password, masterusername))
		self.conn.commit()



	