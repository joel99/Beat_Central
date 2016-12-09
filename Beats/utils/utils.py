import hashlib, sqlite3
import database

#Account Management---------------------------------------------------------
#given login information, check database
def isValidLogin(userName, password):
    return database.isValidAccountInfo(userName, hashed(password))

def verify(userID, oldPass, pass1, pass2):
    return hashed(oldPass) == database.getPass(userID) and pass1 == pass2

def changePass(userID, password):
    return database.changePass(userID, hashed(password))

def getUserID(username):
    return database.getUserID(username)
    
def isValidRegister(pass1, pass2, username):
    return pass1 == pass2 and (not database.doesUserExist(username))

def register(username, password):
    return database.registerAccountInfo(username, hashed(password))

#User interaction
def isFavorited(uID, typeOf, lastID, spotID):
    return database.isFavorited(uID, typeOf, lastID + "_" + spotID)


#HELPERS--------------------------------------
def hashed(unhashed):
    return hashlib.sha512(unhashed).hexdigest()
