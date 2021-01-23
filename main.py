import requests
import json
from sparql import Sparql
from aux_functions import *

prefixes = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX mov: <http://www.semanticweb.org/daniel/ontologies/moviesAndSeries#>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>"""

moviesList = []
filmesAlugados = []

def getMoviesObject():
    sparql = Sparql()
    moviesSelect = sparql.select("""SELECT ?movie ?name WHERE {
            ?movie rdf:type mov:Movie .
            ?movie foaf:name ?name
            }
    """)
    
    movies = moviesSelect['results']['bindings']

    for movie in movies:
        idMovie = movie['movie']['value']
        name = movie['name']['value']
        moviesList.append({ 'movieprefix': idMovie, 'moviename': name})

def getFilmesAlugados():
    sparql = Sparql()
    moviesAlugados = sparql.select("""SELECT ?movieid ?moviename (GROUP_CONCAT(?cid;SEPARATOR=', ') AS ?consumerid) (GROUP_CONCAT(?cname; SEPARATOR=', ') as ?consumername) WHERE {
            ?movieid rdf:type mov:Movie .
            ?movieid foaf:name ?moviename .
            ?movieid mov:alugadoPor ?cid .
            ?cid foaf:name ?cname
        } GROUP BY ?movieid ?moviename
    """)
    
    movies = moviesAlugados['results']['bindings']
    for movie in movies:
        moviename = movie['moviename']['value']
        consumers = (movie['consumername']['value']).split(', ')
        filmesAlugados.append({ 'moviename': moviename, 'consumers': consumers })

    # for movie in movies:
    #     idMovie = movie['movie']['value']
    #     name = movie['name']['value']
    #     moviesList.append({ 'movieprefix': idMovie, 'moviename': name})
    

def menu_add_consumer():
    getMoviesObject()

    for index, item in enumerate(moviesList):
        moviePrefix = item['movieprefix'].split('#')[1]
        print(f'{index+1} - {moviePrefix} ({item["moviename"]})')

    movieIndexId = int(input('Seleccione o index do filme: '))-1
    selectedMovie = moviesList[movieIndexId]['movieprefix'].split('#')[1]
    
    consumerName = input('Nome do cliente: ')
    consumerNameId = 'mov:consumer_' + remove_characters_except_number_letter(consumerName)

    consumerInsert = Sparql()
    consumerExists = consumerInsert.ask(f'ASK {{ {consumerNameId} rdf:type mov:Consumer }}')

    if not consumerExists:
        consumerInsert.insertTriple(f'{consumerNameId} rdf:type mov:Consumer')
        consumerInsert.insertTriple(f'{consumerNameId} foaf:name "{consumerName}"')

    consumerInsert.insertTriple(f'mov:{selectedMovie} mov:alugadoPor {consumerNameId}')

def menu_filmes_alugados():
    getFilmesAlugados()

    for item in filmesAlugados:
        print(f'* {item["moviename"]}')
        print('  (filme alugado por)')
        for consumer in item['consumers']:
            print(f'   - {consumer}')
            
        print('\n')

def menu_entry():
    choice = '0'

    while choice == '0':
        print('1) Add consumer')
        print('2) Filmes alugados')

        choice = input('Select an option: ')

        if choice == '1':
            menu_add_consumer()

        if choice == '2':
            menu_filmes_alugados()

def main():
    menu_entry()

main()