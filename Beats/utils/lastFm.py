# Please use an identifiable User-Agent header on all requests.
#^^^This implies that I need to keep the urrlib2 header identifier,
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
def songSearch(name, artist=None):
    query_d = {"method": "track.search", "track": name, "api_key": API_KEY,
               "format": "json"}
    if artist != None:
        query_d["artist"] = artist
    res = rest.get(API_ROOT, query_d)  # User-agent header should be default
    if res["type"] == "HTTPError" or res["type"] == "URLError":
        # returning (status, result); error already sent to console
        return ("Error", [])
    res_dict = json.loads(res["object"].read())
    if "error" in res_dict:
        err_str = "ERROR: lastFm.songSearch() for '" + name + "'"
        if artist != None:
            err_str += ", by '" + artist + "'"
        err_str += " resulted in an API error/\n"
        err_str += "\t Code: " + str(res_dict["error"])
        err_str += "; Message: " + res_dict["message"]
        print err_str
        # returning (status, result); error already sent to console
        return ("Error", [])
    result_list = []
    for track in res_dict["results"]["trackmatches"]["track"]:
        result_list.append(build_track_dict(track))
    return ("OK", result_list)


def build_track_dict(track):
    track_dict = {
        "name": track["name"], "artist": track["artist"], "mbid": track["mbid"]
    }
    if "image" in track:
        img_url = ""
        img_size = ""
        for img_dict in track["image"]:
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
            track_dict["image"] = img_url
            track_dict["image_size"] = img_size
    return track_dict
