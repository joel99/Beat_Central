import database, spotify, lastFm

def getSearch(q, searchType):
    if searchType == 0:
        searchResults = lastFm.songSearch(q)
    if searchType == 1:
        searchResults = lastFm.artistSearch(q)
    if searchType == 2:
        searchResults = lastFm.albumSearch(q)
        
    if (searchResults[0] == "Error"):
        return "Error"
    else:
        if len(searchResults[1]) == 0:
            return "Empty"
        else:
            return searchResults[1]

#urls serve as ids
def toggleFavorite(userID, favType, entry, entryUrl):
    if database.isFavorited(userID, favType, entry, entryUrl):
        database.rmFavorite(userID, favType, entry, entryUrl)
    else:
        database.addFavorite(userID, favType, entry, entryUrl)

def getFavorites(typeOf, userID):
    #first retrieve database entry, then pass to spotify
    if typeOf == 0:
        favList = [0, database.getFavorites(userID, 'Songs')]
    elif typeOf == 1:
        favList = [1, database.getFavorites(userID, 'Artists')]
    else:
        favList = [2, database.getFavorites(userID, 'Albums')]

    return favList	

def contentGen(typeOf, lastFmID): #id is a string
    typeOf = typeOf.lower()
    #lastFmID is of the form: 1 for has ID, 0 for no ID.
    #noID keys are of the form artist/name (if it has name)
    ided = lastFmID[0]
    lastFmKey = lastFmID[1:]
    if ided == "1":
        if typeOf == "song":
            lastContent = lastFm.getSongInfo(lastFmID)
        elif typeOf == "artist":
            lastContent = lastFm.getArtistInfo(lastFmID)
        else:
            lastContent = lastFm.getAlbumInfo(lastFmID)
            #type, name, artist
    else:
        if typeOf == "song" or typeOf == "album":
            lastList = lastFmKey.split('/')
            if typeOf == "song":
                lastContent = lastFm.getSongInfo(None, lastDict[0], lastDict[1])
            else:
                lastContent = lastFm.getAlbumInfo(None, lastDict[0], lastDict[1])
        else:
            lastContent = lastFm.getSongInfo(None, lastFmKey)
    
    if typeOf == "song" or typeOf == "album":
        name = lastContent["name"]
        art = lastContent["artist"]
    else:
        name = lastContent["name"]
        art = None
    spotContent = spotify.getItemUri(typeOf, name, art)
    
    return [lastContent, spotContent]
