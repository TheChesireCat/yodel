import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import re
import requests
from BeautifulSoup import BeautifulSoup as bs
import BeautifulSoup
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

def listSongs(query):
    mov_url=extractMovieUrl(query)
    print "URL : ",mov_url
    url = mov_url + "soundtrack"
    req = requests.get(url)
    result = req.content
    soup = bs(result)
    names=[]
    for song in soup.findAll("div", {"id" : re.compile('sn[0-9]*')}):
        text = song.contents
        name_list = []
        name_list.append(i[0])
        name=''
        for i in text:
            if isinstance(i,BeautifulSoup.Tag):
		        name+=i.text
            elif isinstance(i,BeautifulSoup.NavigableString):
		        name+=str(i)
        name_list.append(name)
        print "Title : ",name_list[0],"\nDescription : \n",name_list[1]
        names.append(name_list)
    return names
