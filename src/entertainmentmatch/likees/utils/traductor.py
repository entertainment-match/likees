#!/usr/bin/env python
# Este archivo usa el encoding: utf-8
'''
Created on 29/11/2010

@author: rcruzper
'''
from entertainmentmatch.likees.models import Movie
#import freebase
import simplejson
import urllib2
#import re	

class Idioma:
    def __init__(self, idioma, url, patron, wikipedia):
        self.idioma = idioma
        self.url = url
        self.patron = patron
        self.wikipedia = wikipedia

#def wikipedia_main():
#    url_en = 'http://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content&format=xml&pageids='
#    url_es = 'http://es.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content&format=xml&pageids='
#    url_fr = 'http://fr.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content&format=xml&pageids='
#    
#    en = "en"
#    es = "es"
#    fr = "fr"
#    
#    patron_en = '\| name\s*=\s(.*)'
#    patron_es = '\| título\s*=\s(.*)'
#    patron_fr = '\| titre\s*=\s(.*)' 
#
#    wikipedia_en = '/wikipedia/en_id'
#    wikipedia_es = '/wikipedia/es_id'
#    wikipedia_fr = '/wikipedia/fr_id'
#    
#    idioma_en = Idioma(en, url_en, patron_en, wikipedia_en)
#    idioma_es = Idioma(es, url_es, patron_es, wikipedia_es)
#    idioma_fr = Idioma(fr, url_fr, patron_fr, wikipedia_fr)
#    
#    idiomas = [idioma_en, idioma_fr]
#    
#    movies = Movie.objects.all().order_by('-tmdb_votes_count')[:10];
#    
#    for movie in movies:
#        print movie.original_name.encode('utf-8')
#        if movie.id_imdb is None:
#            continue
#        
##        print 'imdb:' + movie.id_imdb + ':'
#
#        
#        imdb = '/authority/imdb/title/' + movie.id_imdb
#        json = freebase.mqlread({"id":imdb,"type": "/film/film","key": [{"*": []}]})
#                
#        for idioma in idiomas:
#            try:
#                page_lan_id = None
##                print json
#                for j in json['key']:
#                    if j['namespace'][0] == idioma.wikipedia:
#                        page_lan_id = j['value']
#                        break
#                
#                if page_lan_id is not None:
##                    print idioma.url + page_lan_id
#                    html = urllib2.urlopen(idioma.url + page_lan_id)
#                    
#                    title_es = None
#                    for linia2 in html:
#                        regex = re.compile(idioma.patron)
#                        r = regex.search(linia2)
#                        if r is not None:
#                            title_es = r.group(1)
#                            title_es = title_es.replace('%20', ' ')
#                            title_es = title_es.replace('\n', '')
#                            print idioma.idioma + ': ' + title_es
#                            encontrado = True
#                            break
#                        
#                    if not encontrado:
#                        print idioma.idioma + ': error:' + idioma.url + page_lan_id
#            except Exception as ex:
#                print idioma.idioma + ': error'
#                print ex
#                pass
    

#def freebase_main():
#    result = ''
#    f = open('error.txt', "w")
#    
#    i = 0
#    movies = Movie.objects.all().order_by('-votes_count');
#    
#    for movie in movies:
#        i = i + 1
#        try:
#            multiidiomas = Multilanguage.objects.filter(code=movie.name_code_m, language='es')
#            
#            multiidioma = None
#            
#            for multiidioma_aux in multiidiomas:
#                multiidioma = multiidioma_aux
#    
#            if multiidioma is None:
#                imdb = '/authority/imdb/title/' + movie.id_imdb
#                json = freebase.mqlread({"id":imdb,"name":[{}]})
#                
#                encontrado = False
#                for j in json['name']:
#                    if j['lang'] == '/lang/es':
#                        encontrado = True
#                    
#                if encontrado == False:
#                    result = result + ' No se ha encontrado el idioma - ' + movie.name_default_m + '<br>'
#                    f.write('No se ha encontrado el idioma - ' + movie.name_default_m + '\n')
#                       
#        except:
#            result = result + ' Error desconocido - ' + movie.name_default_m + '<br>'
#            f.write('Error desconocido - ' + movie.name_default_m + '\n')
#        
#        if i == 10:
#            f.close()
#            break
    
#    return result

def prueba():
#    api = 'apikeythemoviedb'
    path = 'http://api.themoviedb.org/2.1/Movie.getTranslations/en/json/apikeythemoviedb/'
    lista_idiomas = ['en', 'es']
    movies = Movie.objects.all()[:1000]

    for movie in movies:
        try:
            print movie.original_name
            id = str(movie.id_tmdb)
    #        print path + id
            request = urllib2.urlopen(path + id)
            json = simplejson.load(request)
            
            lista_idiomas_encontrados = []
            for j in json:
                for translation in j['translations']:
                    idioma = translation['iso_639_1']
                    if idioma in lista_idiomas:
                        print 'idioma encontrado: ' + idioma
                        lista_idiomas_encontrados.append(translation['iso_639_1'])
        except:
            pass
