
# Module Utils, File lastFm.py
# last.fm API functions
# Team Bass Drop - Beat Central

# Please use an identifiable User-Agent header on all requests.
# ^^^This implies that I need to keep the urrlib2 header identifier,
#   and use add_header for our header/auth purposes?
# Use MKotlik last.fm account for API account

import rest
import json

# API_KEY is temporarily harcoded, will later be moved to outside file
API_KEY = "42becc236bc618eb1ba223b81fa9e4f8"
API_ROOT = "http://ws.audioscrobbler.com/2.0/"


# NOTES:
# NOTE: Should probably give url to lastfm in all responses
# TODO: implement key error catching in all search/info funcs
# TODO: test what corrections does
# NOTE: should we link to artist from tracks in get albums? no good for spotify


# ======MAIN METHODS====== #


def songSearch(name, artist=None, page=1):
    """Search for a track by track name.

    Employs the lastFm track.search endpoint to provide a formatted list of
    tracks related to the query, ordered by relevance. Returns a complex
    object.

    Args:
        name (str): name of the track
        artist (str, optional): if song artist is provided, will be used in
            search. Defaults to None.
        page (int, optional): page of results to be retrieved, in increments of
            30 results. Defaults to 1.

    Returns:
        tuple: a complex object, whose first element is a status set to 'Error'
            or 'OK', depending on the success of the operation.

        The second element of the tuple is a list of dictionaries, where each
        dictionary corresponds to one result. If the list is empty, no results
        were found for the given query.

        Each dictionary contains the 'name', 'artist', and 'mbid' properties.
        If the result included images, an image url will be given as 'image',
        and the image size will be provided as 'image_size'. Images can be of
        size 'medium', 'large', or 'small', in that order of preference. If no
        image was found, the 'image' key will not be present in
        the result dict.

        If an error occurs during the request, the status (first) element of
        the returned tuple will be "Error", and a detailed error message will
        be logged in the console.

        The returned object structure is as follows::

            ("<OK | ERROR>", [
                    {
                        "name":"<TRACK NAME>", "artist":"<ARTIST NAME>",
                        "mbid":"<MBID>", "image":"<IMAGE URL>",
                        "image_size":"<IMAGE SIZE>"
                    },
                    {
                        "name":"<TRACK NAME>", "artist":"<ARTIST NAME>",
                        "mbid":"<MBID>"
                    }
                ]
            )
    """
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
        print build_API_error(res_dict, "songSearch", name=name, artist=artist)
        # returning (status, result); error already sent to console
        return ("Error", [])
    results_list = []
    for track in res_dict["results"]["trackmatches"]["track"]:
        if track["mbid"] != "":
            results_list.append(build_track_album_dict(track))
    return ("OK", results_list)


def albumSearch(name, page=1):
    """Search for an album by album name.

    Employs the lastFm album.search endpoint to provide a formatted list of
    albums related to the query, ordered by relevance. Returns a complex
    object.

    Args:
        name (str): name of the album
        page (int, optional): page of results to be retrieved, in increments of
            30 results. Defaults to 1.

    Returns:
        tuple: a complex object, whose first element is a status set to 'Error'
            or 'OK', depending on the success of the operation.

        The second element of the tuple is a list of dictionaries, where each
        dictionary corresponds to one result. If the list is empty, no results
        were found for the given query.

        Each dictionary contains the 'name' and 'mbid' properties.
        If the result included images, an image url will be given as 'image',
        and the image size will be provided as 'image_size'. Images can be of
        size 'medium', 'large', or 'small', in that order of preference. If no
        image was found, the 'image' key will not be present in
        the result dict.

        If an error occurs during the request, the status (first) element of
        the returned tuple will be "Error", and a detailed error message will
        be logged in the console.

        The returned object structure is as follows::

            ("<OK | ERROR>", [
                    {
                        "name":"<ALBUM NAME>", "mbid":"<MBID>",
                        "image":"<IMAGE URL>", "image_size":"<IMAGE SIZE>"
                    },
                    {
                        "name":"<ALBUM NAME>", "mbid":"<MBID>"
                    }
                ]
            )
    """
    query_d = {"method": "album.search", "album": name, "api_key": API_KEY,
               "format": "json", "page": page, "limit": 30}
    # User-agent header should be default
    res = rest.get(API_ROOT, query_d)
    if res["type"] == "HTTPError" or res["type"] == "URLError":
            # returning (status, result); error already sent to console
        return ("Error", [])
    res_dict = json.loads(res["object"].read())
    if "error" in res_dict:
        print build_API_error(res_dict, "albumSearch", name=name)
        # returning (status, result); error already sent to console
        return ("Error", [])
    results_list = []
    for album in res_dict["results"]["albummatches"]["album"]:
        if album["mbid"] != "":
            results_list.append(build_track_album_dict(album))
    return ("OK", results_list)


def artistSearch(name, page=1):
    """Search for an artist by artist name.

    Employs the lastFm artist.search endpoint to provide a formatted list of
    artists related to the query, ordered by relevance. Returns a complex
    object.

    Args:
        name (str): name of the artist
        page (int, optional): page of results to be retrieved, in increments of
            30 results. Defaults to 1.

    Returns:
        tuple: a complex object, whose first element is a status set to 'Error'
            or 'OK', depending on the success of the operation.

        The second element of the tuple is a list of dictionaries, where each
        dictionary corresponds to one result. If the list is empty, no results
        were found for the given query.

        Each dictionary contains the 'name' and 'mbid' properties.
        If the result included images, an image url will be given as 'image',
        and the image size will be provided as 'image_size'. Images can be of
        size 'medium', 'large', or 'small', in that order of preference. If no
        image was found, the 'image' key will not be present in
        the result dict.

        If an error occurs during the request, the status (first) element of
        the returned tuple will be "Error", and a detailed error message will
        be logged in the console.

        The returned object structure is as follows::

            ("<OK | ERROR>", [
                    {
                        "name":"<ARTIST NAME>", "mbid":"<MBID>",
                        "image":"<IMAGE URL>", "image_size":"<IMAGE SIZE>"
                    },
                    {
                        "name":"<ARTIST NAME>", "mbid":"<MBID>"
                    }
                ]
            )
    """
    query_d = {"method": "artist.search", "artist": name, "api_key": API_KEY,
               "format": "json", "page": page, "limit": 30}
    # User-agent header should be default
    res = rest.get(API_ROOT, query_d)
    if res["type"] == "HTTPError" or res["type"] == "URLError":
            # returning (status, result); error already sent to console
        return ("Error", [])
    res_dict = json.loads(res["object"].read())
    if "error" in res_dict:
        print build_API_error(res_dict, "artistSearch", name=name)
        # returning (status, result); error already sent to console
        return ("Error", [])
    results_list = []
    for artist in res_dict["results"]["artistmatches"]["artist"]:
        if artist["mbid"] != "":
            results_list.append(build_artist_dict(artist))
    return ("OK", results_list)


def getSongInfoByID(mbid):
    return getSongInfo(mbid)


def getSongInfoByName(name, artist):
    return getSongInfo(None, name, artist)


def getAlbumInfoByID(mbid):
    return getAlbumInfo(mbid)


def getAlbumInfoByName(name, artist):
    return getAlbumInfo(None, name, artist)


def getArtistInfoByID(mbid):
    return getArtistInfo(mbid)


def getArtistInfoByName(name):
    return getArtistInfo(None, name)


def getSongInfo(mbid=None, name=None, artist=None):
    query_d = {"method": "track.getinfo", "api_key": API_KEY,
               "format": "json"}
    if mbid is not None:
        query_d["mbid"] = mbid
    elif name is not None and artist is not None:
        query_d["track"] = name
        query_d["artist"] = artist
    # User-agent header should be default
    res = rest.get(API_ROOT, query_d)
    if res["type"] == "HTTPError" or res["type"] == "URLError":
            # returning (status, result); error already sent to console
        return ("Error", {})
    res_dict = json.loads(res["object"].read())
    if "error" in res_dict:
        print build_API_error(res_dict, "getSongInfo", mbid=mbid, name=name)
        # returning (status, result); error already sent to console
        return ("Error", {})
    if res_dict["track"]["name"] == "None":
        return ("OK", {})
    return ("OK", build_song_info_dict(res_dict["track"]))


def getAlbumInfo(mbid=None, name=None, artist=None):
    query_d = {"method": "album.getinfo", "api_key": API_KEY,
               "format": "json"}
    if mbid is not None:
        query_d["mbid"] = mbid
    elif name is not None and artist is not None:
        query_d["album"] = name
        query_d["artist"] = artist
    # User-agent header should be default
    res = rest.get(API_ROOT, query_d)
    if res["type"] == "HTTPError" or res["type"] == "URLError":
            # returning (status, result); error already sent to console
        return ("Error", {})
    res_dict = json.loads(res["object"].read())
    if "error" in res_dict:
        print build_API_error(res_dict, "getAlbumInfo", mbid=mbid, name=name)
        # returning (status, result); error already sent to console
        return ("Error", {})
    if res_dict["album"]["name"] == "None":
        # Aka API returned default NONE album
        return ("OK", {})
    return ("OK", build_album_info_dict(res_dict["album"]))


def getArtistInfo(mbid=None, name=None):
    # TODO: Add getTopTags, getTopAlbums, and getSimilar
    query_d = {"method": "artist.getinfo", "api_key": API_KEY,
               "format": "json"}
    if mbid is not None:
        query_d["mbid"] = mbid
    elif name is not None:
        query_d["artist"] = name
    # User-agent header should be default
    res = rest.get(API_ROOT, query_d)
    if res["type"] == "HTTPError" or res["type"] == "URLError":
            # returning (status, result); error already sent to console
        return ("Error", {})
    res_dict = json.loads(res["object"].read())
    if "error" in res_dict:
        print build_API_error(res_dict, "getArtistInfo", mbid=mbid, name=name)
        # returning (status, result); error already sent to console
        return ("Error", {})
    if res_dict["artist"]["name"] == "None":
        return ("OK", {})
    return ("OK", build_artist_info_dict(res_dict["artist"]))


def build_artist_info_dict(artist):
    info_dict = {
        "name": artist["name"], "listeners": artist["stats"]["listeners"],
        "playcount": artist["stats"]["playcount"]
    }
    if "mbid" in artist:
        # DO NOT ASSUME mbid will always be here
        info_dict["mbid"] = artist["mbid"]
    if "bio" in artist:
        # BIO WILL ALWAYS BE THERE, BUT COULD BE EMPTY
        # TODO: CHECK NOT EMPTY BEFORE ADDING, or ASK CONTENT.PY TO CHECK
        info_dict["bio"] = artist["bio"]["content"]
        info_dict["summary"] = artist["bio"]["summary"]
    if "image" in artist:
        img_tuple = get_info_image(artist)
        if img_tuple[0] != "":
            # aka size is extralarge, large, or medium only
            (info_dict["image"], info_dict["image_size"]) = img_tuple
    if "similar" in artist:
        info_dict["similar"] = []
        for sim_art in artist["similar"]["artist"]:
            entry = {"name": sim_art["name"]}
            if "image" in sim_art:
                img_tuple = get_info_image(artist)
                if img_tuple[0] != "":
                    # aka size is extralarge, large, or medium only
                    (entry["image"], entry["image_size"]) = img_tuple
            info_dict["similar"].append(entry)
    if "tags" in artist:
        # NOTE, this is not the same as topTags, which we might need as well
        info_dict["tags"] = []
        for tag in artist["tags"]["tag"]:
            info_dict["tags"].append(tag["name"])
    return info_dict


def build_album_info_dict(album):
    info_dict = {
        "name": album["name"], "artist": album["artist"],
        "listeners": album["listeners"], "playcount": album["playcount"]
    }
    if "mbid" in album:
        # DO NOT ASSUME mbid will always be here
        info_dict["mbid"] = album["mbid"]
    if "releasedate" in album:
        info_dict["releasedate"] = album["releasedate"]
    if "wiki" in album:
        # TODO: either here or in content.py, check that wikis/bios not empty
        info_dict["wiki"] = album["wiki"]["content"]
        info_dict["summary"] = album["wiki"]["summary"]
    if "image" in album:
        img_tuple = get_info_image(album)
        if img_tuple[0] != "":
            # aka size is extralarge, large, or medium only
            (info_dict["image"], info_dict["image_size"]) = img_tuple
    if "tracks" in album:
        info_dict["tracks"] = []
        for track in album["tracks"]["track"]:
            entry = {"name": track["name"], "artist": track["artist"]["name"]}
            if "duration" in track:
                entry["duration"] = track["duration"]
            info_dict["tracks"].append(entry)
    if "tags" in album:
        # NOTE: according to docs, could be "toptags" instead of "tags"
        # NOTE: this is not the same as topTags, which we might need as well
        info_dict["tags"] = []
        for tag in album["tags"]["tag"]:
            info_dict["tags"].append(tag["name"])
    return info_dict


def build_song_info_dict(track):
    info_dict = {
        "name": track["name"], "artist": track["artist"]["name"],
        "listeners": track["listeners"], "playcount": track["playcount"]
    }
    # NOTE: use listening stats from lastfm or spotify?
    if "mbid" in track:
        # DO NOT ASSUME mbid will always be here
        info_dict["mbid"] = track["mbid"]
    if "mbid" in track["artist"]:
        info_dict["artist_mbid"] = track["artist"]["mbid"]
    if "duration" in track:
        # NOTE: use duration from lastfm or spotify?
        info_dict["duration"] = track["duration"]
    if "wiki" in track:
        # TODO: either here or in content.py, check that wikis/bios not empty
        info_dict["wiki"] = track["wiki"]["content"]
        info_dict["summary"] = track["wiki"]["summary"]
    if "album" in track:
        info_dict["album"] = {"name": track["album"][
            "title"], "artist": track["album"]["artist"]}
        if "mbid" in track["album"]:
            info_dict["album"]["mbid"] = track["album"]["mbid"]
        if "image" in track["album"]:
            img_tuple = get_info_image(track["album"])
            if img_tuple[0] != "":
                # aka size is extralarge, large, or medium only
                (info_dict["album"]["image"], info_dict[
                 "album"]["image_size"]) = img_tuple
    if "toptags" in track:
        # NOTE: not the same as topTags endpoint, which we might use instead
        info_dict["tags"] = []
        for tag in track["toptags"]["tag"]:
            info_dict["tags"].append(tag["name"])
    return info_dict


def get_info_image(item):
    img_url, img_size = "", ""
    for img_dict in item["image"]:
        if img_dict["size"] == "medium" and img_size != "large":
            img_url = img_dict["#text"]
            img_size = img_dict["size"]
        if img_dict["size"] == "large" or img_dict["size"] == "extralarge":
            img_url = img_dict["#text"]
            img_size = img_dict["size"]
        if img_dict["size"] == "extralarge":
            break
        # Mega and small are too large and too small respectively
    return (img_url, img_size)

# ======HELPER FUNCTIONS====== #


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


def build_API_error(res_dict, function, mbid=None, name=None, artist=None):
    err_str = "ERROR: lastFm." + function + "() for '"
    if mbid is not None:
        err_str += "mbid: " + mbid + "'"
    else:
        err_str += name + "'"
    if artist is not None:
        err_str += ", by '" + artist + "'"
    err_str += " resulted in an API error/\n"
    err_str += "\t Code: " + str(res_dict["error"])
    err_str += "; Message: " + res_dict["message"]
    return err_str
