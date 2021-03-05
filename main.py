from gui import LoginGUI
from database import Database
from encryption import Encrypter

encrypter = Encrypter()
db = Database("Passwords.db", encrypter)
LoginGUI(db)