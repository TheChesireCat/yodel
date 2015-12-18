import requests
from BeautifulSoup import BeautifulSoup as bs
import sys
if (sys.version_info > (3,0)):
    from urllib.request import urlopen
    from urllib.parse import quote_plus as qp
    raw_input = input
else:
    from urllib2 import urlopen
    from urllib import quote_plus as qp
goog_url = "http://www.google.com/search?q="
you_url="https://www.youtube.com/results?search_query="

def extractMovieUrl(query):
    url = goog_url + qp(query)
    req = requests.get(url)
    result = req.content
    link_start = result.find("http://www.imdb.com")
    link_end = result.find("&amp",link_start)
    link = result[link_start:link_end]
    return link

def listSongs(link):
    url =
