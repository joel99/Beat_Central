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
        userID = 1
    else:
        userID = sel[0] + 1
        
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
    c.execute(cmd)
    db.commit()
    db.close()
    

#UserInfo Table -----------------------------------------------------
#favType expects 'Songs', 'Artists', or 'Albums'
#entries are delimited by '::'

def isFavorited(userID, favType, entry, entryID):
    db = sqlite3.connect("data/main.db")
    c = db.cursor()
    cmd = "SELECT fav%s FROM UserInfo WHERE UserID = %d;"%(favType, userID)
    favs = c.execute(cmd).fetchone() #is the string
    db.close()
    return entry + entryID in favs.split('::')
    
#does not have isFavorited check
def addFavorite(userID, favType, entry, entryID):
    db = sqlite3.connect("data/main.db")
    c = db.cursor()
    #first get the relevant info
    cmd = "SELECT fav%s FROM UserInfo WHERE UserID = %d;"%(favType, userID)
    oldFavs = c.execute(cmd).fetchone() #is the string
    entry = entry + '~~' + entryID
    if len(oldFavs) > 0:
        newFavs = oldFavs + "::" + entry 
    else:
        newFavs = entry
    cmd = "UPDATE UserInfo SET fav%s='%s' WHERE UserID = %d;"%(favType, newFavs, userID)
    c.execute(cmd)
    db.commit()
    db.close()

def rmFavorite(userID, favType, entry, entryID):
    db = sqlite3.connect("data/main.db")
    c = db.cursor()
    #first get the relevant info
    cmd = "SELECT fav%s FROM UserInfo WHERE UserID = %d;"%(favType, userID)
    oldFavs = c.execute(cmd).fetchone() #is the string
    splitFavs = oldFavs.split('::').remove(entry + entryID)
    newFavs = '::'.join(splitFavs)
    cmd = "UPDATE UserInfo SET fav%s='%s' WHERE UserID = %d;"%(favType, newFavs, userID)
    c.execute(cmd)
    db.commit()
    db.close()

#returns list of tuples
def getFavorites(userID, favType):
    db = sqlite3.connect("data/main.db")
    c = db.cursor()
    #first get the relevant info
    cmd = "SELECT fav%s FROM UserInfo WHERE UserID = %d;"%(favType, userID)
    sel = c.execute(cmd).fetchone() #the relevant string
    db.close()
    strDict = sel.split('::')
    ret = []
    for entry in strDict:
        ret.add(entry.split('~~'))
    return ret


#following
def follow(fromID, followID):
    db = sqlite3.connect("data/main.db")
    c = db.cursor()
    #first get the relevant info
    cmd = "SELECT following FROM UserInfo WHERE UserID = %d;"%(fromID)
    sel = c.execute(cmd).fetchone() #the relevant string
    if len(sel) > 0:
        sel = sel + "::" + followID
    else:
        sel = followID
    cmd = "UPDATE UserInfo SET following='%s' WHERE UserID = %d;"%(sel, fromID)
    c.execute(cmd)
    db.commit()
    db.close()
        
def rmFollow(fromID, followID):
    db = sqlite3.connect("data/main.db")
    c = db.cursor()
    #first get the relevant info
    cmd = "SELECT following FROM UserInfo WHERE UserID = %d;"%(fromID)
    sel = c.execute(cmd).fetchone() #the relevant string
    split = sel.split('::').remove(followID)
    newList = '::'.join(split)
    cmd = "UPDATE UserInfo SET following='%s' WHERE UserID = %d;"%(sel, fromID)
    c.execute(cmd)
    db.commit()
    db.close()


def getFollowing(fromID):
    db = sqlite3.connect("data/main.db")
    c = db.cursor()
    #first get the relevant info
    cmd = "SELECT following FROM UserInfo WHERE UserID = %d;"%(fromID)
    sel = c.execute(cmd).fetchone() #the relevant string
    db.close()
    return sel


def isFollowing(fromID, followID):
    db = sqlite3.connect("data/main.db")
    c = db.cursor()
    #first get the relevant info
    cmd = "SELECT following FROM UserInfo WHERE UserID = %d;"%(fromID)
    sel = c.execute(cmd).fetchone() #the relevant string
    db.close()
    return followID in sel.split('::') 
