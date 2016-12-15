
# Module Utils, File rest.py
# API backend functions
# Team Bass Drop - Beat Central

from urllib2 import Request, urlopen, URLError, HTTPError
from urllib import urlencode


def get(url, query=None, headers=None):
    try:
        req = Request(url + format_query(query))
        if headers is not None:
            for key in headers:
                req.add_header(key, headers[key])
        response = urlopen(req)
    except HTTPError as e:
        print "ERROR: rest.get() on " + url + " resulted in HTTPError/"
        print "\t " + explain_error(e)
        return {"type": "HTTPError", "object": e}
    except URLError as e:
        print "ERROR: rest.get() on " + url + " resulted in URLError/"
        print "\t " + explain_error(e)
        return {"type": "URLError", "object": e}
    else:
        return {"type": "response", "object": response}


def post(url, body, query=None, headers=None):
    try:
        req = Request(url + format_query(query), urlencode(body))
        if headers is not None:
            for key in headers:
                req.add_header(key, headers[key])
        response = urlopen(req)
    except HTTPError as e:
        print "ERROR: rest.post() on " + url + " resulted in HTTPError/"
        print "\t " + explain_error(e)
        return {"type": "HTTPError", "object": e}
    except URLError as e:
        print "ERROR: rest.post() on " + url + " resulted in URLError/"
        print "\t " + explain_error(e)
        return {"type": "URLError", "object": e}
    else:
        return {"type": "response", "object": response}


def format_query(query):
    if query is not None:
        enc_query = {}
        for key in query:
            enc_query[unicode(key).encode("utf-8")
                      ] = unicode(query[key]).encode("utf-8")
        return "?" + urlencode(enc_query)
    else:
        return ""


def explain_error(e):
    err_str = ""
    if hasattr(e, 'code'):
        err_str += "Code: " + str(e.code) + "; "
    if hasattr(e, 'reason'):
        err_str += "Reason: " + str(e.reason) + ";"
    return err_str
