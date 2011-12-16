from django.db.models import Q
from entertainmentmatch.likees.models import Movie, Person, Category
from htmlentitydefs import name2codepoint as n2cp
import urllib2
import random
from datetime import date
import re


def generate_index(filename):
    
    file = open(filename, "w")

    dates = date.today()
    dates = dates.strftime("%Y-%m-%d")

    content = []
    content.append('<?xml version="1.0" encoding="UTF-8"?>\n\r')
    content.append('<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    content.append('<sitemap>')
    content.append('<loc>http://www.likees.org/sitemap.movies.xml.gz</loc>')
    content.append('<lastmod>'+dates+'</lastmod>')
    content.append('</sitemap>')
 
    content.append('<sitemap>')
    content.append('<loc>http://www.likees.org/sitemap.movies_es.xml.gz</loc>')
    content.append('<lastmod>'+dates+'</lastmod>')
    content.append('</sitemap>')
    
    content.append('<sitemap>')
    content.append('<loc>http://www.likees.org/sitemap.categories.xml</loc>')
    content.append('<lastmod>'+dates+'</lastmod>')
    content.append('</sitemap>')
    
    content.append('<sitemap>')
    content.append('<loc>http://www.likees.org/sitemap.categories_es.xml</loc>')
    content.append('<lastmod>'+dates+'</lastmod>')
    content.append('</sitemap>')

    content.append('<sitemap>')
    content.append('<loc>http://www.likees.org/sitemap.person1.xml.gz</loc>')
    content.append('<lastmod>'+dates+'</lastmod>')
    content.append('</sitemap>')
    
    content.append('<sitemap>')
    content.append('<loc>http://www.likees.org/sitemap.person1_es.xml.gz</loc>')
    content.append('<lastmod>'+dates+'</lastmod>')
    content.append('</sitemap>')
    
    content.append('<sitemap>')
    content.append('<loc>http://www.likees.org/sitemap.person2.xml.gz</loc>')
    content.append('<lastmod>'+dates+'</lastmod>')
    content.append('</sitemap>')
    
    content.append('<sitemap>')
    content.append('<loc>http://www.likees.org/sitemap.person2_es.xml.gz</loc>')
    content.append('<lastmod>'+dates+'</lastmod>')
    content.append('</sitemap>')
    
    content.append('<sitemap>')
    content.append('<loc>http://www.likees.org/sitemap.home.xml</loc>')
    content.append('<lastmod>'+dates+'</lastmod>')
    content.append('</sitemap>')

    content.append('<sitemap>')
    content.append('<loc>http://www.likees.org/sitemap.home_es.xml</loc>')
    content.append('<lastmod>'+dates+'</lastmod>')
    content.append('</sitemap>')
    content.append('</sitemapindex>')

    file.writelines(content)
    file.close()

def generate_movies(filename, lang=None):
    language='?'
    if lang is not None:
        language = '?language='+lang
    file = open(filename, "w")

    dates = date.today()
    dates = dates.strftime("%Y-%m-%d")
    content = []
    content.append('<?xml version="1.0" encoding="UTF-8"?>\n')
    content.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    
    movies = Movie.objects.filter(Q(priority__lt=5)&Q(deleted=0)).order_by('-rating', '-priority')
    for movie in movies:
        try:
            name = movie.normalized_name()
            content.append('<url>')
            # TODO title movie
            content.append('<loc>http://www.likees.org/item/'+str(movie.id)+'/title/'+str(name)+'/'+language+'</loc>')
            content.append('<lastmod>'+dates+'</lastmod>')
            content.append('<changefreq>weekly</changefreq>')
            content.append('<priority>0.9</priority>')
            content.append('</url>')
        except UnicodeEncodeError:
            print movie.id
    content.append('</urlset>')

    file.writelines(content)
    file.close()

def generate_categories(filename, lang=None):
    language='?'
    if lang is not None:
        language = '?language='+lang
    file = open(filename, "w")

    dates = date.today()
    dates = dates.strftime("%Y-%m-%d")
    content = []
    content.append('<?xml version="1.0" encoding="UTF-8"?>\n')
    content.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    
    categories = Category.objects.all()
    for category in categories:
        content.append('<url>')
        content.append('<loc>http://www.likees.org/category/' + str(category.id) + '/'+language+'</loc>')
        content.append('<lastmod>'+dates+'</lastmod>')
        content.append('<changefreq>monthly</changefreq>')
        content.append('<priority>0.9</priority>')
        content.append('</url>')
   
    content.append('</urlset>')

    file.writelines(content)
    file.close()

def generate_home(filename, lang=None):
    if lang is None:
        lang = 'en'
    language = '?language='+lang

    file = open(filename, "w")

    dates = date.today()
    dates = dates.strftime("%Y-%m-%d")
    content = []
    content.append('<?xml version="1.0" encoding="UTF-8"?>\n')
    content.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    content.append('<url>')
    content.append('<loc>http://www.likees.org/'+language+'</loc>')
    content.append('<lastmod>'+dates+'</lastmod>')
    content.append('<changefreq>daily</changefreq>')
    content.append('<priority>1</priority>')
    content.append('</url>')
    content.append('<url>')
    content.append('<loc>http://www.likees.org/movies/'+language+'</loc>')
    content.append('<lastmod>'+dates+'</lastmod>')
    content.append('<changefreq>daily</changefreq>')
    content.append('<priority>1</priority>')
    content.append('</url>')
    content.append('<url>')
    content.append('<loc>http://www.likees.org/movies/'+language+'&amp;from=1950&amp;to=2011&amp;category=&amp;orderby=news</loc>')
    content.append('<lastmod>'+dates+'</lastmod>')
    content.append('<changefreq>always</changefreq>')
    content.append('<priority>0.9</priority>')
    content.append('</url>')
    content.append('<url>')
    content.append('<loc>http://www.likees.org/movies/'+language+'&amp;from=1950&amp;to=2012&amp;category=&amp;orderby=brate</loc>')
    content.append('<lastmod>'+dates+'</lastmod>')
    content.append('<changefreq>always</changefreq>')
    content.append('<priority>0.9</priority>')
    content.append('</url>')
   
    content.append('</urlset>')

    file.writelines(content)
    file.close()


def generate_person(filename1, filename2, lang=None):
    language='?'
    if lang is not None:
        language = '?language='+lang
    file1 = open(filename1, "w")
    file2 = open(filename2, "w")

    dates = date.today()
    dates = dates.strftime("%Y-%m-%d")
    content1 = []
    content2 = []
    content1.append('<?xml version="1.0" encoding="UTF-8"?>\n')
    content1.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    
    content2.append('<?xml version="1.0" encoding="UTF-8"?>\n')
    content2.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    i = 0
    people = Person.objects.all()
    for person in people:
        if i%2 == 1:
            content1.append('<url>')
            content1.append('<loc>http://www.likees.org/person/'+str(person.id)+'/'+language+'</loc>')
            content1.append('<lastmod>'+dates+'</lastmod>')
            content1.append('<changefreq>monthly</changefreq>')
            content1.append('<priority>0.9</priority>')
            content1.append('</url>')
        else:
            content2.append('<url>')
            content2.append('<loc>http://www.likees.org/person/'+str(person.id)+'/'+language+'</loc>')
            content2.append('<lastmod>'+dates+'</lastmod>')
            content2.append('<changefreq>monthly</changefreq>')
            content2.append('<priority>0.9</priority>')
            content2.append('</url>')
        i+=1
   
    content1.append('</urlset>')
    content2.append('</urlset>')

    file1.writelines(content1)
    file1.close()

    file2.writelines(content2)
    file2.close()

def main():
    file_index = "media/sitemap.xml"
    file_categories = "media/sitemap.categories.xml"
    file_home = "media/sitemap.home.xml"
    file_movies = "media/sitemap.movies.xml"
    file_person1 = "media/sitemap.person1.xml"
    file_person2 = "media/sitemap.person2.xml"
    
    file_categories_es = "media/sitemap.categories_es.xml"
    file_home_es = "media/sitemap.home_es.xml"
    file_movies_es = "media/sitemap.movies_es.xml"
    file_person1_es = "media/sitemap.person1_es.xml"
    file_person2_es = "media/sitemap.person2_es.xml"


    print "Generating sitemap"

    generate_index(file_index)
    generate_categories(file_categories)
    generate_home(file_home)
    generate_movies(file_movies)
    generate_person(file_person1, file_person2)

    generate_categories(file_categories_es,'es')
    generate_home(file_home_es,'es')
    generate_movies(file_movies_es,'es')
    generate_person(file_person1_es, file_person2_es,'es')

              

