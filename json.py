# -*- coding: utf-8 -*-
# version 1.0
# Author Ankit Ramakrishnan
# email : aliceoxenbury@gmail.com
import os, sys, re, requests, json
import BeautifulSoup
from BeautifulSoup import BeautifulSoup as bs
if (sys.version_info > (3,0)):
    from urllib.request import urlopen
    from urllib.parse import quote_plus as qp
    raw_input = input
else:
    from urllib2 import urlopen
    from urllib import quote_plus as qp

goog_url = "http://www.google.com/search?q="
you_url="https://www.youtube.com/results?search_query="

def generateJSON(query):
    info=dict()
    url = goog_url + qp(query)
    info["search_url"]=url
    try:
        result = requests.get(url).content
        link_start = result.find("http://www.imdb.com")
        link_end = result.find("&amp",link_start)
        link = result[link_start,link_end]
        info["imdb_url"]=link
    except requests.exceptions.ConnectionError:
        print """ Not connected to the Internet
                  Please check your Internet Connection

                  Stopping"""
        return 1
    url = url + "soundtrack"
    info["soundtrack_url"]=url
    result=requests.get(url).content
    soup = bs(result)
    movie_name = soup.find("h3",{"itemprop":"name"}).text
    info["movie_name"]=movie_name
    songs=[]
    for idx,song in enumerate(soup.findAll("div", {"id" : re.compile('sn[0-9]*')})):
        song_info=dict()
        text = song.contents
        song_info["track_no"]=idx
        song_info["song_name"]=text[0]
        text_blurb=''
        for i in text:
            if isinstance(i,BeautifulSoup.Tag):
		        text_blurb+=i.text.decode('utf-8')
            elif isinstance(i,BeautifulSoup.NavigableString):
		        text_blurb+=str(i).decode('utf-8'
        song_info["text_blurb"]=text_blurb
        query=''
        query+=text[0]
        r = re.search('Performed by (.*)',text_blurb)
        if r is not None:
            song_info["performed_by"]=r.group(1)
            query=query+' '+r.group(1)
        else :
            song_info["performed_by"]=""
        r = re.search('Written and Performed by (.*)',text_blurb)
        if r is not None:
            song_info["written_and_performed_by"]=r.group(1)
            query=query+' '+r.group(1)
        else :
            song_info["written_and_performed_by"]=""
        r = re.search('from the motion picture (.*)',text_blurb)
        if r is not None:
            song_info["motion_picture"]=r.group(1)
            query=query+' '+r.group(1)
        else :
            song_info["motion_picture"]=""
        r = re.search('Music by (.*)',text_blurb)
        if r is not None:
            song_info["music_by"]=r.group(1)
            query=query+' '+r.group(1)
        else :
            song_info["music_by"]=""
        r = re.search('Composed by (.*)',text_blurb)
        if r is not None:
            song_info["composed_by"]=r.group(1)
            query=query+' '+r.group(1)
        else :
            song_info["composed_by"]=""
        query.decode('utf-8')
        result=requests.get(you_url+qp(query))
        link_start=result.find('/watch?v=')
        link_end=result.find('"',link_start+1)
        uri=result[link_start:link_end]
        if uri is not '':
            link='http://www.youtube.com'+uri
        else:
            link=""
        song_info["youtube_url"]=link
        song_info["query"]=query
        songs.append[song_info]
        with open('yodel.json','w') as outfile:
            json.dump(info,outfile)
        return json.dumps(info)
