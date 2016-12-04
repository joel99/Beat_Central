import hashlib, sqlite3
import database

#given login information, check database
def isValidLogin(userName, password):
    hashedPass = hashlib.sha512(password).hexdigest()
    return database.isValidAccountInfo(userName, hashedPass)

def getUserID(username):
    return database.getUserID(username)
    
#making new account
def isValidRegister(pass1, pass2, username):
    #also do database checks
    return pass1 == pass2 and (not database.doesUserExist(username))

def register(username, password):
    hashedPass = hashlib.sha512(password).hexdigest()
    return database.registerAccountInfo(username, hashedPass)
