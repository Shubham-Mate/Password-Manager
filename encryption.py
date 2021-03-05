import string

# Substitution cipher
class Encrypter:
	def __init__(self):
		self.key = 'QAg7ZDBxHOamTYMVXPIE2eJ0wKqltpNdzLW4nvbShUc3Gjfsk98ruRyCF1i65o'
		self.ascii_string = string.ascii_letters + string.digits
		self.encrypt_pairs = {}
		self.decrypt_pairs = {}
		for key, value in zip(self.ascii_string, self.key):
			self.encrypt_pairs[key] = value
			self.decrypt_pairs[value] = key

	def encrypt(self, string):
		new_str = ''
		for char in string:
			new_str += self.encrypt_pairs[char]
		return new_str

	def decrypt(self, string):
		new_str = ''
		for char in string:
			new_str += self.decrypt_pairs[char]
		return new_str
