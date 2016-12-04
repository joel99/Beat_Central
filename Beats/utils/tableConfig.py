#Initializes database

import sqlite3

db = sqlite3.connect("../data/main.db")
c = db.cursor()

peopleTable = "CREATE TABLE UserInfo(userID INTEGER, following TEXT, favSongs TEXT, favArtists TEXT, favAlbums TEXT);"
c.execute(peopleTable)

accntTable = "CREATE TABLE AccountInfo(username TEXT, hashedPass TEXT, userID INTEGER);"
c.execute(accntTable)

db.commit()
db.close()
