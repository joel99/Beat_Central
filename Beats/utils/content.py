import database, spotify, lastFm

def getFollowFeed():
    return None

def getSongs(q):
    searchResults = spotify.songSearch(q)
    #songSearch will give me a list of tuples
    return searchResults

def getArtists(q):
    searchResults = spotify.artistSearch(q)
    return searchResults

def getAlbums(q):
    searchResults = spotify.albumSearch(q)
    return searchResults

def toggleFavorite(userID, favType, entry, entryID):
    if database.isFavorited(userID, favType, entry, entryID):
        database.rmFavorite(userID, favType, entry, entryID)
    else:
        database.addFavorite(userID, favType, entry, entryID)
'''
def getFavorites(typeOf, userID):
        #first retrieve database entry, then pass to spotify
    if typeOf == 0:
        favList = database.getFavorites(userID, 'Songs')
    elif typeOf == 1:
        favList = database.getFavorites(userID, 'Artists')
    else:
        favList = database.getFavorites(userID, 'Albums')
    ret = []    
    for entry in favList:
        ret.add(spotify.search(typeOf, entry[1])
    return ret	
'''
def contentGen(lastFmID, spotifyID):
    lastContent = lastFm.getContent(lastFmID)
    spotContent = spotify.getContent(spotifyID)
