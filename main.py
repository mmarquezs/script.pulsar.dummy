import sys
import json
import base64
import re
import urllib
import urllib2
import bencode
import hashlib

PAYLOAD = json.loads(base64.b64decode(sys.argv[1]))


def torrent2magnet(torrent_url):
  response = urllib2.urlopen(torrent_url)
  torrent = response.read()
  metadata = bencode.bdecode(torrent)
  hashcontents = bencode.bencode(metadata['info'])
  digest = hashlib.sha1(hashcontents).digest()
  b32hash = base64.b32encode(digest)
  magneturl = 'magnet:?xt=urn:btih:' + b32hash  + '&dn=' + metadata['info']['name']
  return magneturl


def search(query):
    response = urllib2.urlopen("http://www.newpct.com/buscar-descargas/%s" % urllib.quote_plus(query))
    data = response.read()
    if response.headers.get("Content-Encoding", "") == "gzip":
        import zlib
        data = zlib.decompressobj(16 + zlib.MAX_WBITS).decompress(data)
    sections = (data.split("<td"))
    uris = []
        
    for section in sections:
        torrent = re.compile(r'http[s]?://.*\.torrent').search(section)
        if torrent != None:
            uris.append({"uri": torrent2magnet(torrent.group(0))})
    return uris

def search_episode(imdb_id, tvdb_id, name, season, episode):
    return search("%s S%02dE%02d" % (name, season, episode))


def search_movie(imdb_id, name, year):
    imdb_id='tt0111161'
    response = urllib2.urlopen("http://www.myapifilms.com/imdb?idIMDB=%s&lang=es-es" % urllib.quote_plus(imdb_id))
    data = json.load(response)
    return search(data['title'])

urllib2.urlopen(
    PAYLOAD["callback_url"],
    data=json.dumps(globals()[PAYLOAD["method"]](*PAYLOAD["args"]))
)
