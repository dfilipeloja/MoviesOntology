import pandas
import requests
import json

prefixes = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX rent: <http://www.semanticweb.org/daniel/ontologies/moviesAndSeries#>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>"""

data_filename = 'movies.csv'
endpoint = 'http://localhost:3030/bdsproject/'

rental_prefix = 'rent:rental_'

def insertTriple(triple):
    response = requests.post(endpoint + 'update', data = { 'update': prefixes + ' INSERT DATA{ ' + triple + '}'})
    if response.status_code == 200:
        print('[OK_200]: ' + triple)
    else:
        print('[FAIL_400]: ' + triple)
        print(response.reason)


def insertMovieTitle(rentalId, name):
    insertTriple(f'{rentalId} foaf:name \'{name}\'')


def insertRental(rentalId):
    insertTriple(f'{rentalId} rdf:type rent:Rental')


def insertActors(actors):
    pass


def insertDirectors(directors):
    pass


def insertGenre(genre):
    pass


def main():
    rental_id = rental_prefix
    table = pandas.read_csv(data_filename, sep='\t')
    
    for index, row in table.iterrows():
        movieTitle = row['Title'].replace(' ', '')
        rental_id += movieTitle

        insertRental(rental_id)
        insertMovieTitle(rental_id, movieTitle)
        # add more relations
        # break

main()