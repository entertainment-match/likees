

import json
import datetime
from entertainmentmatch.likees.models import Item, Movie, Company, Role, Job, Person, Multilanguage, Item_Job_Cast_Person, Cast, Image, Category, Country, Item_ReleaseDate_Country, ReleaseDate


def getMultiCode():
    multiLatest = None
    try:
        multiLatest = Multilanguage.objects.order_by("-id")[0]
    except:
        print "Se ha producido un error."
        
    code_latest = 0
    if multiLatest is not None:
        code_latest = multiLatest.code
        
    return code_latest +1

def createMovie(entrada):
    print('Result: ' + entrada['titulo'])
    
    # Realizamos la carga de Item-Pelicula

    lang = entrada['language']
    name_code_m = getMultiCode()
    name_default_m = entrada['original_name']
    alternative_code_m = getMultiCode()
    alternative_name_m = entrada['alternative_name']
    overview_code_m = getMultiCode()
    overview_name_m = entrada['overview']
    tagline_code_m = getMultiCode()
    tagline_default_m = entrada['tagline']
    
    multiOriginalName = Multilanguage(code=name_code_m, language=lang, literal=name_default_m)
    multiOriginalName.save()
    
    multiAlternativeName = Multilanguage(code=alternative_code_m, language=lang, literal=alternative_name_m)
    multiAlternativeName.save()
    
    multiOverview = Multilanguage(code=overview_code_m, language=lang, literal=overview_name_m)
    multiOverview.save()
    
    tagline = Multilanguage(code=tagline_code_m, language=lang, literal=tagline_default_m)
    tagline.save()
    
    imageThumb = Image(url=entrada['image":{"type":"poster","size":"cover'],date=datetime.date.today())
    imageThumb.save()
    
    imageBig = Image(url=entrada['image":{"type":"poster","size":"mid'],date=datetime.date.today())
    imageThumb.save()
    
    categories = [] 
    
    for category in entrada['genres']:
        categs = Category.objects.filter(name_default_m=category['name'])
        for cat in categs:
            cat_code_m = getMultiCode()
            cat_name_m = category['name']
            categoryMult = Multilanguage(code=cat_code_m, language=lang, literal=cat_name_m)
            categoryMult.save()
            cat = Category(name_code_m=cat_code_m, name_default_m=cat_name_m)
            cat.save()
        
        categories.append(cat)
        

    
    #Company.objects.get()
    
    item = Movie(released=entrada['released'], 
                homepage=entrada['homepage'],
                votes_count=entrada['votes'],
                version=entrada['version'],
                name_code_m=name_code_m,
                name_default_m=name_default_m,
                alternative_code_m=alternative_code_m,
                overview_code_m=overview_code_m,
                overview_name_m=overview_name_m,
                tagline_code_m=tagline_code_m,
                tagline_default_m=tagline_default_m,
                type=entrada['type'],
                image=imageBig,
                thumb=imageThumb,
                runtime=entrada['runtime'],
                trailer=entrada['trailer'],
                id_imdb=entrada['imdb_id'],
                id_tmdb=entrada['id'],
                categories = categories
                )
    

def main():
    
    with open('input/item.json', mode='r', encoding='utf-8') as f:
        entrada = json.load(f) 
    
    print('Cadena:' + entrada)
    
    #entrada = json.loads(json.dumps({'titulo':'titulo peli'}))
    createMovie(entrada)


    
if __name__ == "__main__":
    main()