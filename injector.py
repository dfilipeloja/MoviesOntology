import pandas
import requests
import json

prefixes = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX mov: <http://www.semanticweb.org/daniel/ontologies/moviesAndSeries#>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>"""

data_filename = 'movies.csv'
endpoint = 'http://localhost:3030/bdsproject/'

rental_prefix = 'mov:rental_'

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


def select(triple):
    response = requests.post(endpoint + 'query', data = { 'query' : prefixes + triple })
    print(response.json())


def insertMovieTitle(rentalId, name):
    insertTriple(f'{rentalId} rdf:type mov:Movie')
    insertTriple(f'{rentalId} foaf:name \'{name}\'')


def insertRental(rentalId):
    insertTriple(f'{rentalId} rdf:type mov:Rental')


def insertActors(actors):
    pass


def insertDirectors(rental_id, directors):
    #se não existe
    #directorId -> mov:director_daniel
    insertTriple(f'{directors} rdf:type mov:Director')
    insertTriple(f'{directors} foaf:name {directorName}')
    insertTriple(f'{directors} mov:realizou {rental_id}')
    
    pass


def insertGenre(genre):
    pass


def main():
    select('SELECT ?subject WHERE { ?subject rdf:type mov:Director }')
    select('SELECT ?subject WHERE { ?subject rdf:type mov:Consumer }')
    select('ASK { mov:daniel rdf:type mov:Consumer }')
    select('ASK { mov:daniel rdf:type mov:Director }')


    rental_id = rental_prefix
    table = pandas.read_csv(data_filename, sep='\t')
    
    for index, row in table.iterrows():
        movieTitle = row['Title'].replace(' ', '')
        rental_id += movieTitle

        insertRental(rental_id)
        insertMovieTitle(rental_id, movieTitle)
        insertDirectors(rental_id, row['Director'])
        # add more relations
        # break

main()