# coding=<latin1>

import json
import os, glob
import datetime
from entertainmentmatch.likees.models import Movie, Image, Category, Country, Person, Job, Item_Job_Cast_Person, Company, Role
import shutil
from django.db import transaction

path = '/home/likees/backup_tmdb/'
path_error = '/home/likees/backup_tmdb/error/'
path_success = '/home/likees/backup_tmdb/success/'
path_adult = '/home/likees/backup_tmdb/adult/'
path_sporting_film = '/home/likees/backup_tmdb/sporting_event/'
path_fan_film = '/home/likees/backup_tmdb/fan_film/'
code_latest = 0

class AdultException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class SportingEventException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
    
class FanFilmException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class PersonException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

@transaction.commit_on_success
def createMovie(entradas):
    # Realizamos la carga de Item-Pelicula
    for entrada in entradas:
        
        if entrada['adult']:
            raise AdultException('adult = true')
            break

        # Movie type, ignoramos series de peliculas
        if entrada['movie_type'] == 'movie series':
            break
 
        # Comprobamos si ya existe la pelicula en la bbdd
        movie = Movie.objects.filter(id_tmdb=entrada['id'])
        
        if not movie:            
            original_name = entrada['original_name']
               
            alternative_name = None
            if entrada['alternative_name'] is not None:
                alternative_name = entrada['alternative_name']
            
            overview_name = None
            if entrada['overview'] is not None:
                overview_name = entrada['overview']
            
            # image
            image_ = None
            thumb_ = None
            for image in entrada['posters']:
                for e in image.values():
                    if thumb_ is None and  e['type'] == 'poster' and e['size'] == 'cover':
                        thumb_ = Image(url=e['url'],date=datetime.date.today())
                        thumb_.save()
                       
                    if image_ is None and e['type'] == 'poster' and e['size'] == 'mid':
                        image_ = Image(url=e['url'],date=datetime.date.today())
                        image_.save()

            
            relDate = '1900-01-01'
            if entrada['released'] is not None and entrada['released'] != '':
                relDate = entrada['released'] 

            # item.
            item = Movie(released=relDate, 
                        homepage=entrada['homepage'],
                        version=entrada['version'],
                        type='Movie',
                        name_en=original_name,
                        original_name=original_name,
                        alternative_name=alternative_name,
                        overview_en=overview_name,
                        tagline_en=entrada['tagline'],
                        runtime=entrada['runtime'],
                        trailer=entrada['trailer'],
                        id_imdb=entrada['imdb_id'],
                        id_tmdb=entrada['id'],
                        image=image_,
                        thumb=thumb_
                        )
            
            item.save()
        
            # categories.
            for category in entrada['genres']:
                if category['name'] == 'Sporting Event':
                    raise SportingEventException('sporting_event = true')

                if category['name'] == 'Fan Film':
                    raise FanFilmException('fan_film = true')
                
                categsR = Category.objects.filter(name_en=category['name'])
                categs = None
                
                if not categsR:
                    categs = Category(name_en=category['name'])
                    categs.save()
            
                if categsR:
                    categs = categsR.get()
                
                if categs is not None:
                    item.categories.add(categs)

            #studios.
            for studio in entrada['studios']:
                studioTemp = Company.objects.filter(name=studio['name'])
                studioR = None

                if not studioTemp:
                    studioR = Company(name=studio['name'])
                    studioR.save()
                
                if studioTemp:
                    studioR = studioTemp.get()
                
                rol = Role(item=item, company=studioR)
                rol.save()
                   

 
            # produced.
            for produced in entrada['countries']:
                countryR = Country.objects.filter(id=produced['code'])
                
                if countryR is not None:
                    for country in countryR:      
                        item.produced.add(country)

            # cast.
            for cast in entrada['cast']:
                personTemp = Person.objects.filter(name=cast['name'])
#                try:
#                    personTemp.get()
#                except:
#                    print personTemp

                personR = None            

                if not personTemp:
                    image_person = None
                    if cast['profile'] is not None and cast['profile'] != '':
                        image_per_str = cast['profile']
                        image_per_str = image_per_str.replace('thumb.jpg', 'profile.jpg')
                        image_person = Image(url=image_per_str,date=datetime.date.today())
                        image_person.save()
                    
                    personR = Person(name=cast['name'],tmdb_id=cast['id'],image=image_person)
                    personR.save()
                    

                if personTemp:
                    personR = personTemp.get()

                #Tenemos en personR la persona dada de alta
                job = cast['job']
                jobTemp = Job.objects.filter(name_en=job)

                jobR = None

                if not jobTemp:
                    jobR = Job(name_en=job)
                    jobR.save()

                if jobTemp:
                    jobR = jobTemp.get()

                ijcp = Item_Job_Cast_Person(person=personR, item=item, job=jobR)
                ijcp.save()
 
            item.save()

            break

def main():
    for infile in glob.glob( os.path.join(path, '*.json') ):
        with open(infile, mode='r') as f:
            try:
                entrada = json.load(f) 
                createMovie(entrada)
                
                str_all = infile.split('/')
                index = len(str_all)
                shutil.move(infile, path_success + str_all[index-1])

                print "Success " + infile
            except AdultException:
                print "Error " + infile + "AdultException"
                
                str_all = infile.split('/')
                index = len(str_all)
                shutil.move(infile, path_adult + str_all[index-1])
                
                pass
            except SportingEventException:
                print "Error " + infile + "SportingEventException"
                
                str_all = infile.split('/')
                index = len(str_all)
                shutil.move(infile, path_sporting_film + str_all[index-1])
                
                pass
            except FanFilmException:
                print "Error " + infile + "FanFilmException"
                
                str_all = infile.split('/')
                index = len(str_all)
                shutil.move(infile, path_fan_film + str_all[index-1])

                pass
            except Exception as ex:
                print "Error " + infile + ": "
                print ex
                
                str_all = infile.split('/')
                index = len(str_all)
                shutil.move(infile, path_error + str_all[index-1])

                pass

    
if __name__ == "__main__":
    main()
