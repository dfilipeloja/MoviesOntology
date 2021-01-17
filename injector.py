import pandas
import requests
import json
from aux_functions import *

prefixes = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX mov: <http://www.semanticweb.org/daniel/ontologies/moviesAndSeries#>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>"""

data_filename = 'movies.csv'
endpoint = 'http://localhost:3030/bdsproject/'

"""
Title	Director	Cast	Country	Year	Genre
"""

def insertTriple(triple):
    response = requests.post(endpoint + 'update', data = { 'update': prefixes + ' INSERT DATA{ ' + triple + '}'})
    if response.status_code == 200:
        print('[OK_200]: ' + triple)
    else:
        print('[FAIL_400]: ' + triple)
        print(response.reason)



def ask(triple):
    response = requests.post(endpoint + 'query', data = { 'query' : prefixes + triple })
    return response.json()['boolean']


def select(triple):
    response = requests.post(endpoint + 'query', data = { 'query' : prefixes + triple })
    print(response.json())


def insertMovieTitle(movieId, name):
    insertTriple(f'{movieId} rdf:type mov:Movie')
    insertTriple(f'{movieId} foaf:name \'{name}\'')


def insertActor(movie_id, actorId, actorName, actorExists):
    if not actorExists:
        insertTriple(f'{actorId} rdf:type mov:Actor')
        insertTriple(f'{actorId} foaf:name "{actorName}"')

    insertTriple(f'{actorId} mov:atuouEm \'{movie_id}\'')


def insertDirector(movie_id, director, directorName, directorExists):
    if not directorExists:
        insertTriple(f'{director} rdf:type mov:Director')
        insertTriple(f'{director} foaf:name "{directorName}"')

    insertTriple(f'{director} mov:realizou {movie_id}')


def insertCountry(movie_id, country, countryName, countryExists):
    if not countryExists:
        insertTriple(f'{country} rdf:type mov:Country')
        insertTriple(f'{country} foaf:name \'{countryName}\'')

    insertTriple(f'{movie_id} mov:origemEm {country}')


def insertDate(movie_id, date):
    insertTriple(f'{movie_id} mov:data_estreia \'{date}\'')


def insertGenre(movie_id, genre, genreName, genreExists):
    if not genreExists:
        insertTriple(f'{genre} rdf:type mov:Genre')
        insertTriple(f'{genre} foaf:name \'{genreName}\'')

    insertTriple(f'{movie_id} mov:temGeneroDe {genre}')


def main():
    # select('SELECT ?subject WHERE { ?subject rdf:type mov:Director }')
    # select('SELECT ?subject WHERE { ?subject rdf:type mov:Consumer }')
    # ask('ASK { mov:daniel rdf:type mov:Consumer }')
    # ask('ASK { mov:daniel rdf:type mov:Director }')

    movie_prefix = 'mov:movie_'
    director_prefix = 'mov:director_'
    actor_prefix = 'mov:actor_'
    country_prefix = 'mov:country_'
    genre_prefix = 'mov:genre_'

    table = pandas.read_csv(data_filename, sep='\t')
    
    for index, row in table.iterrows():
        movieTitle = row['Title']
        movie_id = movie_prefix + remove_characters_except_number_letter(movieTitle)

        insertMovieTitle(movie_id, movieTitle)

        directors = get_things_split(row['Director'])
        cast = get_things_split(row['Cast'])
        countries = get_things_split(row['Country'])
        date = row['Year']
        genre = row['Genre'].strip()

        for director in directors:
            directorId = remove_characters_except_number_letter(director)
            directorId = director_prefix + directorId

            director = director.strip()

            directorExists = ask(f'ASK {{ {directorId} rdf:type mov:Director }}')
            insertDirector(movie_id, directorId, director, directorExists)

        for actor in cast:
            actorId = remove_characters_except_number_letter(actor)
            actorId = actor_prefix + actorId

            actor = actor.strip()

            actorExists = ask(f'ASK {{ {actorId} rdf:type mov:Actor }}')
            insertActor(movie_id, actorId, actor, actorExists)

        for country in countries:
            countryId = remove_characters_except_number_letter(country)
            countryId = country_prefix + countryId

            country = country.strip()

            countryExists = ask(f'ASK {{ {countryId} rdf:type mov:Country }}')
            insertCountry(movie_id, countryId, country, countryExists)

        insertDate(movie_id, date)

        genreId = remove_characters_except_number_letter(genre)
        genreId = genre_prefix + genreId

        genreExists = ask(f'ASK {{ {genreId} rdf:type mov:Genre }}')

        insertGenre(movie_id, genreId, genre, genreExists)

        #break
    

main()