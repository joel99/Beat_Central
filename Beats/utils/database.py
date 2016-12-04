import sqlite3

#AccountInfo Table -----------------------------------------------------
def isValidAccountInfo(uN, hP):
    db = sqlite3.connect("data/main.db")
    c = db.cursor()

    cmd = "SELECT * FROM AccountInfo WHERE username = '%s' AND hashedPass = '%s';"%(uN, hP)
    sel = c.execute(cmd).fetchone()
    db.close()
    if sel == None:
        return False
    return True

def getUserID(uN):
    db = sqlite3.connect("data/main.db")
    c = db.cursor()
    cmd = "SELECT * FROM AccountInfo WHERE username = '%s';"%(uN)
    sel = c.execute(cmd).fetchone()
    db.close()
    return sel[2]

def registerAccountInfo(uN, hP):
    db = sqlite3.connect("data/main.db")
    c = db.cursor()

    cmd = "SELECT userID FROM AccountInfo ORDER BY userID DESC;"
    sel = c.execute(cmd).fetchone()
    if sel == None: #non-null
        userID = sel[0] + 1
    else:
        userID = 1
        
    addAT = "INSERT INTO AccountInfo VALUES ('%s','%s',%d);"%(uN,hP,userID)
    c.execute(addAT)

    default = ""
    
    addPT = "INSERT INTO UserInfo VALUES (%d,'%s', '%s', '%s', '%s');"%(userID, default, default, default, default)

    c.execute(addPT)
    db.commit()
    db.close()

def doesUserExist(uN):
    db = sqlite3.connect("data/main.db")
    c = db.cursor()
    cmd = "SELECT * FROM AccountInfo WHERE username = '%s';"%(uN)
    sel = c.execute(cmd).fetchone()
    db.close()
    if sel == None:
        return False
    else:
        return True 

def getPass(userID):
    db = sqlite3.connect("data/main.db")
    c = db.cursor()
    cmd = "SELECT * FROM AccountInfo WHERE userID = '%s';"%(userID)
    sel = c.execute(cmd).fetchone()
    password = sel[1]
    print password
    db.close()
    return password

def changePass(userID, newPass):
    db = sqlite3.connect("data/main.db")
    c = db.cursor()
    cmd = "UPDATE AccountInfo SET hashedPass = '%s'WHERE UserID = %d;"%(newPass, userID)
    sel = c.execute(cmd)
    db.commit()
    db.close()
    

#UserInfo Table -----------------------------------------------------
