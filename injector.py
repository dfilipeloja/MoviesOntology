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


def insertActors(actors):
    pass


def insertDirector(movie_id, director, directorName):
    #se não existe
    #directorId -> mov:director_daniel
    insertTriple(f'{director} rdf:type mov:Director')
    insertTriple(f'{director} foaf:name \'{directorName}\'')
    insertTriple(f'{director} mov:realizou {movie_id}')
    
    pass


def insertGenre(genre):
    pass


def main():
    # select('SELECT ?subject WHERE { ?subject rdf:type mov:Director }')
    # select('SELECT ?subject WHERE { ?subject rdf:type mov:Consumer }')
    # ask('ASK { mov:daniel rdf:type mov:Consumer }')
    # ask('ASK { mov:daniel rdf:type mov:Director }')

    movie_prefix = 'mov:movie_'
    director_prefix = 'mov:director_'

    table = pandas.read_csv(data_filename, sep='\t')
    
    for index, row in table.iterrows():
        movieTitle = row['Title']
        movie_id = movie_prefix + movieTitle.replace(' ', '').lower()

        insertMovieTitle(movie_id, movieTitle)

        directors = get_people_split(row['Director'])
        directorName = row['Director']

        for director in directors:
            directorId = remove_characters_except_number_letter(director).lower()
            directorId = director_prefix + directorId

            directorExists = ask(f'ASK {{ {directorId} rdf:type mov:Director }}')

            if not directorExists:
                insertDirector(movie_id, directorId, directorName)

        break
    

main()