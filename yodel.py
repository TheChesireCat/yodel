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
    movie_name=soup.find("h3",{"itemprop":"name"}).text
    print "MOVIE : ",movie_name
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
		        name+=str(i).decode('utf-8')
        name_list.append(name)
        name_list.append(movie_name)
        #print "Title : ",name_list[0],"\nDescription : \n",name_list[1]
        names.append(name_list)
    return names

def youtubeSearch(names):
    links=[]
    for name in names:
        query = ''
        query+=name[0].encode('utf-8')
        query=searchFor(query,name[1],'Written by (.*)')
        query=searchFor(query,name[1],'Written and Performed by (.*)')
        query=searchFor(query,name[1],'from the motion picture (.*)')
        query=searchFor(query,name[1],'Music by (.*)')
        query=searchFor(query,name[1],'Composed by (.*)')
        #query+=name[2].encode('utf-8')
        req=requests.get(you_url+qp(query))
        result=req.content
        link_start=result.find('/watch?v=')
        link_end=result.find('"',link_start+1)
        link='www.youtube.com'+result[link_start:link_end]
        print name[0]," : ",result[link_start:link_end]
        print query,'\n'




def searchFor(query,text,reg):
    query+=' '
    r = re.search(reg,text)
    if r is not None:
        query+=r.group(1).encode('utf-8')
    return query


name=raw_input("Enter the Name of a Movie : ")
youtubeSearch(listSongs(name))
