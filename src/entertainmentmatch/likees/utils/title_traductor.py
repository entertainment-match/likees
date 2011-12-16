#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
Created on 07/01/2011

@author: dysphoria
'''
from django.db.models import Q
from entertainmentmatch.likees.models import Movie
from htmlentitydefs import name2codepoint as n2cp
import urllib2
import random
import time
import re

def decode_htmlentities(string):
    def substitute_entity(match):
        ent = match.group(3)
        if match.group(1) == "#":
            # decoding by number
            if match.group(2) == '':
                # number is in decimal
                return unichr(int(ent))
            elif match.group(2) == 'x':
                # number is in hex
                return unichr(int('0x'+ent, 16))
        else:
            # they were using a name
            cp = n2cp.get(ent)
            if cp: return unichr(cp)
            else: return match.group()
    
    entity_re = re.compile(r'&(#?)(x?)(\w+);')
    return entity_re.subn(substitute_entity, string)[0]

def main():
    print "Hello Traductor! Wait..."

    imdb_es = "http://www.imdb.es/title/"

    count = 0

    try:
        movies = Movie.objects.using('likees_pro').filter(Q(name_es=None)&~Q(id_imdb=None)&Q(deleted=0)).order_by('-rating', '-priority')

        for movie in movies:
            if movie.id_imdb is not None and movie.id_imdb != '':
                count = count + 1
                print str(count) + ' - ' +  imdb_es + movie.id_imdb ,
                print "title: '" + movie.name_en + "' =>" ,
                try:
                    html = urllib2.urlopen(imdb_es + movie.id_imdb)
                    for linia in html:
                        if linia.startswith('<title>'):
                            title_imdb = linia.replace('<title>', '')
                            title_imdb = title_imdb.replace('</title>', '')
                            title_imdb = title_imdb.replace('%20', ' ')
                            title_imdb = title_imdb.replace('\n', '')
                            regex = re.compile('(.*)\s\((.*)\)')
                            r = regex.search(title_imdb)
                            if r is not None:
                                title = decode_htmlentities(r.group(1))
                                print "'" + title + "'" ,
                                movie.name_es = title
                                print "Guardando en BD:", 
                                movie.save(using='likees_pro')
                                seconds = 1 #random.randrange(5,10)
                                print "Ok! Sleep: " + str(seconds)
                                time.sleep(seconds)
                                break
                except Exception as ex:
                    print ex
                    pass
                        
    except Exception as ex:
        print ex
        pass
