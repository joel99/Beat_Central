#Please use an identifiable User-Agent header on all requests.
#^^^This implies that I need to keep the urrlib2 header identifier,
#   and use add_header for our header/auth purposes?
#Use MKotlik last.fm account for API account

import rest

#API_KEY is temporarily harcoded, will later be moved to outside file
API_KEY = "42becc236bc618eb1ba223b81fa9e4f8"
API_ROOT = "http://ws.audioscrobbler.com/2.0/"

#Search for a track by track name. Returns track matches sorted by relevance.
def search_songs(name, artist = None):
    query_d = {"method":"track.search", "track":name, "api_key":API_KEY,
               "format":"json"}
    if artist != NONE:
        query_d["artist"] = artist
    url = API_ROOT
    res = rest.get(url, query_d) #User-agent header should be default
    res_type = res["type"]
    if res_type == HTTPError || res_type == URLError:
        return rest.explain_error(res["object"])
    return (res["object"].getcode(), res["object"].info())
