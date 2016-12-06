#Module Utils, File rest.py
#API backend functions
#Team Bass Drop - Beat Central

import urllib2
import urllib

#Maybe should use add_header() instead of headers?

def get(url, query = None, headers = None):
    response = getR(url, query, headers)
    result = {"url":response.geturl(), "headers":response.info(),
              "status":response.getcode(), "body":response.read()}
    return result

def getR(url, query = None, headers = None):
    req = urllib2.Request(url + format_query(query), headers)
    response = urllib2.urlopen(req)
    return response

def post(url, body, query = None, headers = None):
    response = postR(url, body, query, headers)
    result = {"url":response.geturl(), "headers":response.info(),
              "status":response.getcode(), "body":response.read()}
    return result

def postR(url, body, query = None, headers = None):
    data = urllib.urlencode(body)
    req = urllib2.Request(url + format_query(query), data, headers)
    response = urllib2.urlopen(req)
    return response

#How do None types work in python?
def format_query(query):
    q_string = ""
    for key in query:
        q_string += key + query[key] + "&"
        result = q_string[:-1].replace(" ", "+")
        return result
