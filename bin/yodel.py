# -*- coding: utf-8 -*-
# version 1.0
# Author Ankit Ramakrishnan
# email : aliceoxenbury@gmail.com
import os, sys, re
import requests
import json
import BeautifulSoup
import youtube_dl
from requests import *
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

def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')

class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)

def generateJSON(query):
    info=dict()
    url = goog_url + qp(query)
    info["search_url"]=url
    #try:
    result = requests.get(url).content
    link_start = result.find("http://www.imdb.com")
    link_end = result.find("&amp",link_start)
    link = result[link_start:link_end]
    info["imdb_url"]=link
    # except :
    #     print """ Not connected to the Internet
    #               Please check your Internet Connection
    #
    #               Stopping"""
    #     return 1
    url = link + "soundtrack"
    info["soundtrack_url"]=url
    result=requests.get(url).content
    soup = bs(result)
    movie_name = soup.find("h3",{"itemprop":"name"}).text
    info["movie_name"]=movie_name
    songs=[]
    songs_list = soup.findAll("div", {"id" : re.compile('sn[0-9]*')})
    info["number_of_songs"]=len(songs_list)
    for idx,song in enumerate(songs_list):
        fraction = ((idx+1)*1.0)/len(songs_list)
        complete = int(fraction*30)
        empty=30 - complete
        progress_bar = "["+"#"*complete+"."*empty+"] {}%".format(int(fraction*100))
        message = "\rGenerating JSON string : "
        progress_message=message+progress_bar
        sys.stdout.write(progress_message)
        sys.stdout.flush()
        song_info=dict()
        text = song.contents
        song_info["track_no"]=idx+1
        song_info["song_name"]=text[0]
        text_blurb=''
        for i in text:
            if isinstance(i,BeautifulSoup.Tag):
		        text_blurb+=i.text.encode('utf-8')
            elif isinstance(i,BeautifulSoup.NavigableString):
		        text_blurb+=str(i)
        song_info["text_blurb"]=text_blurb
        query=''
        query+=text[0]
        r = re.search('Performed by (.*)',text_blurb)
        if r is not None:
            song_info["performed_by"]=r.group(1)
            query=query+' '+r.group(1).decode('utf-8')
        else :
            song_info["performed_by"]=""
        r = re.search('Written and Performed by (.*)',text_blurb)
        if r is not None:
            song_info["written_and_performed_by"]=r.group(1)
            query=query+' '+r.group(1).decode('utf-8')
        else :
            song_info["written_and_performed_by"]=""
        r = re.search('from the motion picture (.*)',text_blurb)
        if r is not None:
            song_info["motion_picture"]=r.group(1)
            query=query+' '+r.group(1).decode('utf-8')
        else :
            song_info["motion_picture"]=""
        r = re.search('Music by (.*)',text_blurb)
        if r is not None:
            song_info["music_by"]=r.group(1)
            query=query+' '+r.group(1).decode('utf-8')
        else :
            song_info["music_by"]=""
        r = re.search('Composed by (.*)',text_blurb)
        if r is not None:
            song_info["composed_by"]=r.group(1)
            query=query+' '+r.group(1).decode('utf-8')
        else :
            song_info["composed_by"]=""
        query.encode('utf-8')
        result=requests.get(you_url+query).content
        link_start=result.find('/watch?v=')
        link_end=result.find('"',link_start+1)
        uri=result[link_start:link_end]
        if uri is not '':
            link='http://www.youtube.com'+uri
        else:
            link=""
        song_info["youtube_url"]=link
        song_info["query"]=query
        songs.append(song_info)
    info["songs"]=songs
    info["file_name"]=info["movie_name"]+".json"
    with open("../json/"+info['file_name'],'w') as outfile:
        outfile.write(json.dumps(info, indent=4,sort_keys=True))
    return json.dumps(info)

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'progress_hooks': [my_hook],
}


        
def main():
    """
    Main program
    """
    movie_query= ' '.join(sys.argv[1:])
    info=generateJSON(movie_query)
    info=json.loads(info)
    sys.stdout.write('\n')
    print "yodel!   : ",info["movie_name"]
    print "imdb url : ",info["imdb_url"]
    command_arguments = [
    'youtube-dl',
    '--extract-audio',
    '--audio-quality 9',
    '--output ',
    '--audio-format.%(mp3)s'
    ]
    for song in info["songs"]:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([song['youtube_url']])
        



if __name__ == '__main__':
    main()
