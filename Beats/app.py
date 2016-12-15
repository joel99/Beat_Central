from flask import Flask, render_template, request, session, url_for, redirect

from utils import content, utils, lastFm
from json import load

app = Flask(__name__)
app.secret_key = "secrets"

#Site Navigation
@app.route("/")
def root():
    if (not isLoggedIn()):#if you're not logged in
        return render_template('login.html', isLoggedIn = False)
    else:
        #add processing
        return render_template('home.html', isLoggedIn = True)
	
@app.route('/logout/')
def outdir():
    if isLoggedIn():
	logout()
    return redirect(url_for('root'))

@app.route("/login/", methods = ['POST'])
def login():
    d = request.form
    if utils.isValidLogin(d["username"], d["pass"]):
        session["userID"] = utils.getUserID(d["username"])
    return redirect(url_for('root'))

@app.route("/register/", methods = ['POST'])
def register():
    d = request.form
    if utils.isValidRegister(d["pass1"], d["pass2"], d["username"]):
        utils.register(d["username"], d["pass1"])
        session["userID"] = utils.getUserID(d["username"])
    return redirect(url_for('root'))


@app.route('/search/', methods = ['GET'])
def search():
    query =  request.args.get("query")
    matchedSongs = content.getSearch(query, 0)
    matchedArtists = content.getSearch(query, 1)
    matchedAlbums = content.getSearch(query, 2)
    return render_template('search.html', songs = matchedSongs, artists = matchedArtists, albums = matchedAlbums, query = query)

@app.route('/settings/')
def settings():
    if (not isLoggedIn()):
        return redirect(url_for('root'))
    following = content.getFollowFeed()
    return render_template("settings.html", user = getUserID(), isLoggedIn = 'True', followFeed = following)

@app.route('/changePass/', methods = ['POST'])
def changePass():
    if (not isLoggedIn()):
        return redirect(url_for('root'))
    d = request.form # pass, pass1, pass2
    if utils.verify(getUserID(), d["pass"], d["pass1"], d["pass2"]):
        utils.changePass(getUserID(), d["pass1"])
    return redirect(url_for('root'))

#User Interaction
#for favorites display, template gets tuples
@app.route('/search/', methods = ['GET'])
def searchResult():
    q = request.args.get("query")
    #todo, process strings from REST APIs, get favorite data,
    #the following are formatted tuple dictionaries
    searchRet = []
    for i in range(0, 3):
        searchRet.append(content.getSearch(q, i))
    stats = []
    for i in range(0, 3):
        if searchRet[i] == "Error":
            searchRet[i] = None
            stats.append("Error")
        elif searchRet[i] == "Empty":
            searchRet[i] = None
            stats.append("Empty")
        else:
            stats.append("good")
    
    return render_template('search.html', isLoggedIn = str(isLoggedIn()), songList = searchRet[0], artistList = searchRet[1], albumList = searchRet[2], songStatus = stats[0], artistStat = stats[1], albumStats = stats[2])

@app.route('/result/<typeOf>/<lastFmID>')
def resultPage(typeOf,lastFmID):
    res = content.contentGen(typeOf, lastFmID)
    if isLoggedIn():
        isfav = str(utils.isFavorited(getUserID(), typeOf, res[0]["name"], lastFmID))
    else:
        isfav = None
    return render_template('result.html', isLoggedIn = str(isLoggedIn()), typeOf = typeOf, content = res, isFavorited = isfav)

@app.route('/favorite/<favType>/<entry>/<entryID>')
def favorite(favType, entry, entryID):
    entry.replace("%20", " ")
    if (favType == 0): #song
        content.toggleFavorite(getUserID(), 'Songs', entry, entryID)
    if (favType == 1): #artist
        content.toggleFavorite(getUserID(), 'Artists', entry, entryID)
    if (favType == 2): #album
        content.toggleFavorite(getUserID(), 'Albums', entry, entryID)
    return redirect("/favorites")

@app.route('/favorites/')
def favorites():
    if (not isLoggedIn()):
        return redirect(url_for('root'))
    userID = getUserID()
    songs = content.getFavorites(0, userID)
    artists = content.getFavorites(1, userID)
    albums = content.getFavorites(2, userID)
    return render_template('favorites.html', isLoggedIn = str(isLoggedIn()), favSongs = songs, favArtists = artists, favAlbums = albums)
    
#HELPERS-----------------------------------------------------------------------

#lastFm api_key retrieval
@app.before_first_request
def retrieve_key():
    # This code is executed upon 1st request,
    # before first request is processed.
    key = ""
    with open("data/key.json") as key_file:
        key = load(key_file)["key"]
    lastFm.setKey(key)

#Login Helpers
def isLoggedIn():
    return "userID" in session

def getUserID():
    return session["userID"]

def logout():
    session.pop('userID')

if __name__ == "__main__":
    app.debug = True
    app.run()
