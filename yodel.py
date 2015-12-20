# -*- coding: utf-8 -*-
import re
from colorama import init
from termcolor import colored
import os
init()
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
debug=False
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
    print "URL","   : ",colored(mov_url,'green')
    url = mov_url + "soundtrack"
    req = requests.get(url)
    result = req.content
    soup = bs(result)
    movie_name=soup.find("h3",{"itemprop":"name"}).text
    print "MOVIE"," : ",colored(movie_name,'magenta')
    names=[]
    for song in soup.findAll("div", {"id" : re.compile('sn[0-9]*')}):
        text = song.contents
        name_list = []
        name_list.append(text[0].encode('utf-8'))
        name=''
        for i in text:
            if isinstance(i,BeautifulSoup.Tag):
		        name+=i.text.decode('utf-8')
            elif isinstance(i,BeautifulSoup.NavigableString):
		        name+=str(i).decode('utf-8')
        name_list.append(name.encode('utf-8'))
        name_list.append(movie_name)
        #print "Title : ",name_list[0],"\nDescription : \n",name_list[1]
        names.append(name_list)
    return names

def youtubeSearch(names):
    links=[]
    print "\nSONGS"
    for idx,name in enumerate(names):
        query = ''
        query+=name[0]
        query=searchFor(query,name[1],'Performed by (.*)')
        #query=searchFor(query,name[1],'Written by (.*)')
        query=searchFor(query,name[1],'Written and Performed by (.*)')
        query=searchFor(query,name[1],'from the motion picture (.*)')
        query=searchFor(query,name[1],'Music by (.*)')
        query=searchFor(query,name[1],'Composed by (.*)')
        #query+=name[2].encode('utf-8')
        query.decode('utf-8')
        req=requests.get(you_url+qp(query))
        result=req.content
        link_start=result.find('/watch?v=')
        link_end=result.find('"',link_start+1)
        link='www.youtube.com'+result[link_start:link_end]
        if not debug:
            if result[link_start:link_end] is not '':
                print "[{:<3}] {:<45} : {:<30}".format(idx,name[0],colored(result[link_start:link_end],'green'))
            else:
                print "[{:<3}] {:<45}".format(idx,name[0]),": ", colored("Not found",'red')
        else:
            if result[link_start:link_end] is not '':
                print "[{:<3}] {:<45} : {:<30}".format(idx,name[0],colored(result[link_start:link_end],'green'))
                print "Search query : ",query,"\n"
            else:
                print "[{:<3}] {:<45}".format(idx,name[0]),": ", colored("Not found",'red')
                print "Search query : ",query,"\n"
        links.append([name[0],link])
    print len(links)
    return links

def downloadAndTag(links):
    command_tokens = [
    'youtube-dl',
    '--extract-audio',
    '--audio-format mp3',
    '--audio-quality 0',
    '--output '
    ]
    for name,link in links:
        if link is not '':
            command=' '.join(command_tokens)
            command=command+"\""+name+".%(ext)s\" "+link
            print command
            print "Downloading : ",name
            os.system(command)







def searchFor(query,text,reg):
    query+=' '
    r = re.search(reg,text)
    if r is not None:
        query+=re.sub('\(.*\)','',r.group(1).encode('utf-8'))
    return query


movie_query= ' '.join(sys.argv[1:])
if movie_query.find('-d')>=0:
    debug=True
    movie_query=movie_query.replace('-d','')
downloadAndTag(youtubeSearch(listSongs(movie_query)))
