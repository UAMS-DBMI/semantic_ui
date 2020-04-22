#!/usr/bin/env python

from fastapi import FastAPI, HTTPException
from collections import defaultdict
from pydantic import BaseModel
from typing import List
import json
import requests

class Metadata(BaseModel):
    collection: str
    patient_id: str
    disease_type: str
    location: str

def make_sparql_query(query, params={}):
    params = {'query': query}
    headers = {'Accept': 'application/sparql-results+json'}
    r = requests.get('http://localhost:7200/repositories/prism', params=params, headers=headers)
    r.raise_for_status()
    ret = []
    vars = r.json()['head']['vars']
    for row in r.json()['results']['bindings']:
        new_row = {}
        for var in vars:
            new_row[var] = row[var]['value']
        ret.append(new_row)
    return ret

app = FastAPI()

@app.get("/", response_model=List[Metadata])
def query_all_metadata(collection: str = None, disease_type: str = None, location: str = None):
    query = """PREFIX collection: <http://purl.org/PRISM_0000001>
PREFIX inheres: <http://purl.obolibrary.org/obo/RO_0000052>
PREFIX human: <http://purl.obolibrary.org/obo/NCBITaxon_9606>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX identifier: <http://purl.obolibrary.org/obo/IAO_0020000>
PREFIX denotes: <http://purl.obolibrary.org/obo/IAO_0000219>
PREFIX has_part: <http://purl.obolibrary.org/obo/BFO_0000051>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
select ?collection ?patient_id ?disease_type ?location{

    # the collection
    ?cid rdf:type collection: .
    ?cid rdfs:label ?collection .

	# the person
	?person rdf:type human: .
	# the person identifier
    ?id denotes: ?person .
    ?id rdf:type identifier: .
    ?id rdfs:label ?patient_id .

    # parts of this person
 	?person has_part: ?ppart .
    ?ppart rdf:type ?loctype .
    ?loctype rdfs:label ?location .
    # want only the immediate location type -- not superclasses like 'organ subunit'
    FILTER NOT EXISTS{
        ?x rdfs:subClassOf ?loctype.
    }

    ?dis_inst inheres: ?ppart .
    ?dis_inst rdf:type ?dt .
    ?dt rdfs:label ?disease_type .
    # want only the immediate diease type
    FILTER NOT EXISTS{
        ?x rdfs:subClassOf ?dt.
    }

}"""
    return make_sparql_query(query)

@app.get("/locations")
def locations():
    query = """PREFIX human: <http://purl.obolibrary.org/obo/NCBITaxon_9606>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX identifier: <http://purl.obolibrary.org/obo/IAO_0020000>
PREFIX has_part: <http://purl.obolibrary.org/obo/BFO_0000051>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
select distinct ?location{
	# the person
	?person rdf:type human: .
    # parts of this person
 	?person has_part: ?ppart .
    ?ppart rdf:type ?loctype .
    ?loctype rdfs:label ?location .
    # want only the immediate location type -- not superclasses like 'organ subunit'
    FILTER NOT EXISTS{
        ?x rdfs:subClassOf ?loctype.
    }
}"""
    results = make_sparql_query(query)
    return [x['location'] for x in results]

@app.get("/disease_types")
def disease_types():
    query = """PREFIX collection: <http://purl.org/PRISM_0000001>
PREFIX inheres: <http://purl.obolibrary.org/obo/RO_0000052>
PREFIX human: <http://purl.obolibrary.org/obo/NCBITaxon_9606>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX has_part: <http://purl.obolibrary.org/obo/BFO_0000051>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
select distinct ?disease_type {
	# the person
	?person rdf:type human: .
    ?dis_inst inheres: ?ppart .
    ?dis_inst rdf:type ?dt .
    ?dt rdfs:label ?disease_type .
    # want only the immediate diease type
    FILTER NOT EXISTS{
        ?x rdfs:subClassOf ?dt.
    }
}"""
    results = make_sparql_query(query)
    return [x['disease_type'] for x in results]

@app.get("/collections")
def collections():
    query = """PREFIX collection: <http://purl.org/PRISM_0000001>
PREFIX human: <http://purl.obolibrary.org/obo/NCBITaxon_9606>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX has_part: <http://purl.obolibrary.org/obo/BFO_0000051>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
select distinct ?collection {

    # the collection
    ?cid rdf:type collection: .
    ?cid rdfs:label ?collection .
}"""
    results = make_sparql_query(query)
    return [x['collection'] for x in results]
