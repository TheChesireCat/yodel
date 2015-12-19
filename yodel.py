# -*- coding: utf-8 -*-
import re
import sys
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
    try :
        req = requests.get(url)
        result = req.content
        link_start = result.find("http://www.imdb.com")
        link_end = result.find("&amp",link_start)
        link = result[link_start:link_end]
        return link
    except requests.exceptions.ConnectionError:
        print "Not Connected to the Internet, Please check your connection. :(\n\nNon verbose errors may follow\nERRORS :\n"

def listSongs(query):
    mov_url=extractMovieUrl(query)
    print "URL : ",mov_url
    url = mov_url + "soundtrack"
    req = requests.get(url)
    result = req.content
    soup = bs(result)
    print "MOVIE : ",soup.find("h3",{"itemprop":"name"}).text
    names=[]
    for song in soup.findAll("div", {"id" : re.compile('sn[0-9]*')}):
        text = song.contents
        name_list = []
        name_list.append(text[0])
        name=''
        for i in text:
            if isinstance(i,BeautifulSoup.Tag):
		        name+=i.text.encode('utf-8')
            elif isinstance(i,BeautifulSoup.NavigableString):
		        name+=str(i).encode('utf-8')
        name_list.append(name)
        #print "Title : ",name_list[0],"\nDescription : \n",name_list[1]
        names.append(name_list)
    return names
name=raw_input("Enter the Name of a Movie : ")
for index,song in enumerate(listSongs(name)):
    print "[{:^3}] {}".format(index+1,song[0].encode('utf-8'))
