'''
Created on 27/10/2010

@author: apigeon
'''

config = {}
config['apikey'] = "insertar api key de themoviedb"
config['urls'] = {}
config['urls']['movie.search'] = "http://api.themoviedb.org/2.1/Movie.search/en/json/%(apikey)s/%%s" % (config)
config['urls']['movie.getInfo'] = "http://api.themoviedb.org/2.1/Movie.getInfo/en/json/%(apikey)s/%%s" % (config)
config['urls']['media.getInfo'] = "http://api.themoviedb.org/2.1/Media.getInfo/en/json/%(apikey)s/%%s/%%s" % (config)
config['urls']['imdb.lookUp'] = "http://api.themoviedb.org/2.1/Movie.imdbLookup/en/json/%(apikey)s/%%s" % (config)
config['urls']['movie.getLatest'] = "http://api.themoviedb.org/2.1/Movie.getLatest/en/json/%(apikey)s" % (config)

import urllib2, time, json as json_decoder
from entertainmentmatch.likees.models import Movie

class TmdBaseError(Exception):
    pass
class TmdNoResults(TmdBaseError):
    pass
class TmdHttpError(TmdBaseError):
    pass
class TmdXmlError(TmdBaseError):
    pass

class JsonHandler:
    """Deals with retrieval of XML files from API"""
    def __init__(self, url):
        self.url = url

    def _grabUrl(self, url):
        try:
            urlhandle = urllib2.urlopen(url)
        except IOError, errormsg:
            raise TmdHttpError(errormsg)
        if urlhandle.code >= 400:
            raise TmdHttpError("HTTP status code was %d" % urlhandle.code)
        return urlhandle.read()

    def getJson(self, movieId):
        print self.url
        json = self._grabUrl(self.url)
        print json
        return json

def getMovieInfo(movieId):
    """Returns movie info by it's TheMovieDb ID.
    Returns a Movie instance
    """
    try:
        url = config['urls']['movie.getInfo'] % (movieId)
        return JsonHandler(url).getJson(movieId)
    except :
        print 'no se puede encontrar la peli con id =', movieId
    finally:
        pass

def saveMovieInfo(movieId, movieInfo):
    if movieInfo == '["Nothing found."]':
        print "no se guarda informacion"
        return False
    else:
        path = '/home/likees/backup_tmdb/' + str(movieId) + '.json'
        file = open(path, 'w')
        file.write(movieInfo)
        print "informacion guardada en " + path
        return True

def getLatestFromTmdb():
    try:
        url = config['urls']['movie.getLatest']
        latest = JsonHandler(url).getJson(0)
        json = json_decoder.loads(latest)
        for js in json:
            return js['id']

    except:
        print "no se ha podido obtener la ultima pelicula subida a tmdb"
        raise Exception()

def getLatestFromLikees():
    try:
        movies = Movie.objects.all().order_by('-id_tmdb')[:1]
        for movie in movies:
            return movie.id_tmdb

    except:
        print "no se ha podido obtener la ultima pelicula de likees"
        raise Exception()

def getOneId(idTmdb):
    initialId = idTmdb
    finalId = idTmdb

    if initialId > finalId:
        print "no hay nuevas peliculas que descargar"
        raise Exception()

    movieId = initialId
    while movieId <= finalId:
        movieInfo = getMovieInfo(movieId)
        if movieInfo is not None:
            if saveMovieInfo(movieId, movieInfo):
                time.sleep(0)
        movieId = movieId + 1

def main():
    initialId = getLatestFromLikees() + 1
    finalId = getLatestFromTmdb()

    if initialId > finalId:
        print "no hay nuevas peliculas que descargar"
        raise Exception()

    movieId = initialId
    while movieId <= finalId:
        movieInfo = getMovieInfo(movieId)
        if movieInfo is not None:
            if saveMovieInfo(movieId, movieInfo):
                time.sleep(0)
        movieId = movieId + 1
