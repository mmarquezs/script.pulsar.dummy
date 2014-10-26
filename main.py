import sys
import json
import base64
import urllib
import urllib2
import bencode
import hashlib

from pulsar import provider

def extract_torrents(data):
    import re
    for torrent in re.findall(r'http[s]?://.*\.torrent', data):
        yield {"uri": torrent}

def search(query):
    resp = provider.POST("http://www.newpct.com/buscar-descargas/", data="cID=0&tLang=0&oBy=0&oMode=0&category_=All&subcategory_=All&idioma_=1&calidad_=All&oByAux=0&oModeAux=0&size_=0&q=%s" % query)
    return extract_torrents(resp.data)
    
def search_episode(episode):
    return search("%(title)s S%(season)02dE%(episode)02d" % episode)


def search_movie(data):
    language="es"
    url_movie = "http://api.themoviedb.org/3/find/%s?api_key=57983e31fb435df4df77afb854740ea9&language=%s&external_source=imdb_id" % (data['imdb_id'], language)
    movie = urllib2.urlopen(url_movie)
    text1 = json.loads(movie.read())
    text2 = text1['movie_results']
    text3 = text2[0]
    title= text3.get("title")

    return search(title.encode('utf-8'))

provider.register(search, search_movie, search_episode)
