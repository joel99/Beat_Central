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

def contentGen(typeOf, lastFmID):
    lastContent = lastFm.getSongInfo(lastFmID)
    #lastContent["name"] = 
    #type, name, artist
    spotContent = spotify.getItemUri(typeOf.lower())
    return [lastContent, spotContent]
