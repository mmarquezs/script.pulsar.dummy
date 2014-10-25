import urllib2,urllib
import json
imdb_id='tt0111161'
response = urllib2.urlopen("http://www.myapifilms.com/imdb?idIMDB=%s&lang=es-es" % urllib.quote_plus(imdb_id))
data = json.load(response)
print(data['title'])
