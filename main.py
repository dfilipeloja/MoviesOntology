import requests
import json
from sparql import Sparql

prefixes = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX mov: <http://www.semanticweb.org/daniel/ontologies/moviesAndSeries#>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>"""

moviesList = []

def main():
    sparql = Sparql()
    moviesSelect = sparql.select("""SELECT ?movie ?name WHERE {
            ?movie rdf:type mov:Movie .
            ?movie foaf:name ?name
            }
    """)
    
    movies = moviesSelect['results']['bindings']

    for movie in movies:
       # print(movie)
        idMovie = movie['movie']['value']
        name = movie['name']['value']
        moviesList.append({ 'id': idMovie, 'name': name})

    print(moviesList)
main()