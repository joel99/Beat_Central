
# Module Utils, File spotify.py
# spotify API functions
# Team Bass Drop - Beat Central

# Please use an identifiable User-Agent header on all requests.
# ^^^This implies that I need to keep the urrlib2 header identifier,
#   and use add_header for our header/auth purposes?

import rest
import json
from base64 import b64encode

# NOTES:
# NOTE: Access tokens have limited lives, should implement refresh system
# TODO: create before_first_request func in app.py to pass auth info to auth

# GLOBALS:
API_ROOT = "https://api.spotify.com/v1"
# ACCESS_TOKEN = ""

# auth not needed, unable to use market=from_token for improved rates
"""
def auth(client_id, client_secret):
    # returns boolean
    auth_str = b64encode(client_id + ":" + client_secret)
    auth_hdr = {"Authorization": "Basic " + auth_str}
    url = "https://accounts.spotify.com/api/token"
    body = {"grant_type": "client_credentials", "scope": "user-read-private"}
    q_str = {"scope": "user-read-private"}
    res = rest.post(url, body, q_str, auth_hdr)
    if res["type"] == "HTTPError" or res["type"] == "URLError":
        # returning (status, result); error already sent to console
        return False
    res_dict = json.loads(res["object"].read())
    if "error" in res_dict:
        err_str = "ERROR: spotify.auth() failed with error: '"
        err_str += res_dict["error"] + "'/\n & error_description: '"
        err_str += res_dict["error_description"]
        print err_str
        return False
    global ACCESS_TOKEN
    ACCESS_TOKEN = res_dict["access_token"]
    return True
"""

def search(q_type, name, artist=None):
    """ Get 1st search result for album, artist, or track.

    Accepts types: album, artist, and track
    Needs artist for album and track searches

    Returns tuple, where 1st el is status, and second el is 1st search
        result. If empty, no results found.
    """
    url = API_ROOT + "/search"
    # auth_hdr = {"Authorization": "Bearer " + ACCESS_TOKEN}
    query_d = {"type": q_type, "limit": 1}
    # Removed "market": "from_token" for testing
    if q_type == "artist":
        q_str = 'artist:"' + name + '"'
    elif q_type == "album":
        if artist is None:
            print "ERROR: spotify.search() not given artist for album search"
            return ("Error", {})
        q_str = 'album:"' + name + '" artist:"' + artist + '"'
    elif q_type == "track":
        if artist is None:
            print "ERROR: spotify.search() not given artist for track search"
            return ("Error", {})
        q_str = 'track:"' + name + '" artist:"' + artist + '"'
    else:
        print "ERROR: spotify.search() not given proper q_type"
        return ("Error", {})
    query_d["q"] = q_str
    # resp = rest.get(url, query_d, auth_hdr)
    resp = rest.get(url, query_d)
    if resp["type"] == "HTTPError" or resp["type"] == "URLError":
        # returning (status, result); error already sent to console
        return ("Error", {})
    resp_dict = json.loads(resp["object"].read())
    return ("OK", build_result_dict(q_type, resp_dict[q_type + "s"]["items"]))

def build_result_dict(q_type, item_list):
    if len(item_list) == 0:
        return {}
    item = item_list[0]
    res_dict = {"name": item["name"], "type": q_type,
                "uri": item["uri"]}
    if "artists" in item:
        res_dict["artist"] = item["artists"][0]["name"]
    return res_dict

def getItemUri(q_type, name, artist=None):
    """ Returns the Spotify uri for an item

    Args:
        
    
    item = search(q_type, name, artist)
    if item[0] == "Error":
        return ("Error", "")
    return ("OK", item[1]["uri"])
