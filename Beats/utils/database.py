import sqlite3

def isValidAccountInfo(uN, hP):
    db = sqlite3.connect("data/main.db")
    c = db.cursor()

    cmd = "SELECT * FROM AccountInfo WHERE username = '%s' AND hashedPass = '%s';"%(uN, hP)
    sel = c.execute(cmd)
    if (sel.fetchone()): #if it exists
        db.close()
        return True
    db.close()
    return False

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
    sel = c.execute(cmd)
    userID = 1
    for record in sel:
        userID = userID + record[0]
        break
        
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
    ret = ""
    cmd = "SELECT * FROM AccountInfo;"
    sel = c.execute(cmd)
    for record in sel:
        if uN == record[0]:
            db.close()
            return True
    db.close()
    return False
