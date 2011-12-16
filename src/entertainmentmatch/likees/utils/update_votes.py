'''
Created on 18/01/2011

@author: dysphoria
'''
from django.db import connections
from entertainmentmatch.likees.models import Movie

def main():
    cursor = connections['likees_pro'].cursor()
    cursor.execute('select item_id, count(*) as votos from likees_vote group by item_id order by votos desc')
    rows = cursor.fetchall()

    for row in rows:
        movie = Movie.objects.using('likees_pro').get(pk=row[0])
        movie.votes_count = row[1]
        movie.save(using='likees_pro')

if __name__ == "__main__":
    main()