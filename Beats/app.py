from flask import Flask, render_template, request, session, url_for, redirect

from utils import content, utils

app = Flask(__name__)
app.secret_key = "secrets"

@app.route("/")
def root():
    if (not isLoggedIn()):#if you're not logged in
        return render_template('home.html', isLoggedIn = 'False')#change to login.html
    else:
        #add processing
        feedDict = content.getFeed()
        return render_template('home.html', isLoggedIn = 'True', feedEntries = feed)
        

@app.route("/login/", methods = ['POST'])
def login():
    d = request.form
    if utils.isValidLogin(d["username"], d["pass"]):
        session["userID"] = utils.getUserID(d["username"])
    return redirect(url_for('root'))

@app.route("/register/", methods = ['POST'])
def register():
    d = request.form
    if utils.isValidRegister(d["pass1"], d["pass2"], d["username"]):#needs to check databases
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


#HELPERS-----------------------------------------------------------------------
def isLoggedIn():
    return "userID" in session

def getUserID():
    return session["userID"]

if __name__ == "__main__":
    app.debug = True
    app.run()
