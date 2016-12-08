# Please use an identifiable User-Agent header on all requests.
# ^^^This implies that I need to keep the urrlib2 header identifier,
#   and use add_header for our header/auth purposes?
# Use MKotlik last.fm account for API account

import rest
import json

# API_KEY is temporarily harcoded, will later be moved to outside file
API_KEY = "42becc236bc618eb1ba223b81fa9e4f8"
API_ROOT = "http://ws.audioscrobbler.com/2.0/"

# Search for a track by track name. Returns track matches sorted by relevance.
# Returns a tuple, 1st element is status, second element is a
#   list of track dictionaries, sorted by relevance
# If empty list, no matches
# By default, top 30 matches are returned
# Use page, which defaults to 1, to get more results in increments of 30


def songSearch(name, artist=None, page=1):
    query_d = {"method": "track.search", "track": name, "api_key": API_KEY,
               "format": "json", "page": page, "limit": 30}
    if artist is not None:
        query_d["artist"] = artist
    res = rest.get(API_ROOT, query_d)  # User-agent header should be default
    if res["type"] == "HTTPError" or res["type"] == "URLError":
        # returning (status, result); error already sent to console
        return ("Error", [])
    res_dict = json.loads(res["object"].read())
    if "error" in res_dict:
        print build_search_API_error(res_dict, "song", name, artist)
        # returning (status, result); error already sent to console
        return ("Error", [])
    results_list = []
    for track in res_dict["results"]["trackmatches"]["track"]:
        results_list.append(build_track_album_dict(track))
    return ("OK", results_list)


def albumSearch(name, page=1):
    query_d = {"method": "album.search", "album": name, "api_key": API_KEY,
               "format": "json", "page": page, "limit": 30}
    # User-agent header should be default
    res = rest.get(API_ROOT, query_d)
    if res["type"] == "HTTPError" or res["type"] == "URLError":
            # returning (status, result); error already sent to console
        return ("Error", [])
    res_dict = json.loads(res["object"].read())
    if "error" in res_dict:
        print build_search_API_error(res_dict, "album", name)
        # returning (status, result); error already sent to console
        return ("Error", [])
    results_list = []
    for album in res_dict["results"]["albummatches"]["album"]:
        results_list.append(build_track_album_dict(album))
    return ("OK", results_list)


def artistSearch(name, page=1):
    query_d = {"method": "artist.search", "artist": name, "api_key": API_KEY,
               "format": "json", "page": page, "limit": 30}
    # User-agent header should be default
    res = rest.get(API_ROOT, query_d)
    if res["type"] == "HTTPError" or res["type"] == "URLError":
            # returning (status, result); error already sent to console
        return ("Error", [])
    res_dict = json.loads(res["object"].read())
    if "error" in res_dict:
        print build_search_API_error(res_dict, "artist", name)
        # returning (status, result); error already sent to console
        return ("Error", [])
    results_list = []
    for artist in res_dict["results"]["artistmatches"]["artist"]:
        results_list.append(build_artist_dict(artist))
    return ("OK", results_list)


def build_track_album_dict(item):
    item_dict = build_basic_res_dict(item)
    item_dict["artist"] = item["artist"]
    return item_dict


def build_artist_dict(artist):
    return build_basic_res_dict(artist)


def build_basic_res_dict(item):
    item_dict = {
        "name": item["name"], "mbid": item["mbid"]
    }
    if "image" in item:
        img_url = ""
        img_size = ""
        for img_dict in item["image"]:
            if img_dict["size"] == "small" and img_size != "large":
                img_url = img_dict["#text"]
                img_size = img_dict["size"]
            if img_dict["size"] == "large" or img_dict["size"] == "medium":
                img_url = img_dict["#text"]
                img_size = img_dict["size"]
            if img_dict["size"] == "medium":
                break
            # Do not use extralarge images; they waste page load times
        if img_url != "":
            item_dict["image"] = img_url
            item_dict["image_size"] = img_size
    return item_dict


def build_search_API_error(res_dict, search_type, name, artist=None):
    err_str = "ERROR: lastFm." + search_type + "Search() for '" + name + "'"
    if artist is not None:
        err_str += ", by '" + artist + "'"
    err_str += " resulted in an API error/\n"
    err_str += "\t Code: " + str(res_dict["error"])
    err_str += "; Message: " + res_dict["message"]
    return err_str
