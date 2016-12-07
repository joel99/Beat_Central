from flask import Flask, render_template, request, session, url_for, redirect

from utils import content, utils

app = Flask(__name__)
app.secret_key = "secrets"

#Site Navigation
@app.route("/")
def root():
    if (not isLoggedIn()):#if you're not logged in
        return render_template('login.html', isLoggedIn = False)
    else:
        #add processing
        feedDict = content.getFeed()
        return render_template('home.html', isLoggedIn = True, newsFeed = feedDict)
    
@app.route('/toolbar/', methods = ['POST'])
def toolBar():
    d = request.form
    if (d["type"] == "Log In"):
            return redirect(url_for('root'))
    return redirect(url_for('home'))

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
    matchedSongs = content.songSearch(query)
    matchedArtists = content.artistSearch(query)
    matchedAlbums = content.albumSearch(query)
    return render_template('search.html', songs = matchedSongs, artists = matchedArtists, albums = matchedAlbums)


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
    matchedSongs = content.getSongs(q) #(song, artist, isFavorited, songID)
    matchedArtists = content.getArtists(q) #(artist, isFavorited, artistID)
    matchedAlbums = content.getAlbums(q) #(album, artist, isFavorited, albumID)
    return render_template('search.html', isLoggedIn = str(isLoggedIn()), songList = matchedSongs, artistList = matchedArtists, albumList = matchedAlbums)


def resultPage():
    return None


@app.route('/favorite/', methods = ['POST'])
def favorite(favType, entry, entryID):
    if (favType == 0): #song
        content.toggleFavorite(getUserID(), 'Songs', entry, entryID)
    if (favType == 1): #artist
        content.toggleFavorite(getUserID(), 'Artists', entry, entryID)
    if (favType == 2): #album
        content.toggleFavorite(getUserID(), 'Albums', entry, entryID)

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
