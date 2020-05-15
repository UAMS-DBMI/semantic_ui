#!/usr/bin/env python

from fastapi import FastAPI, HTTPException
from collections import defaultdict
from pydantic import BaseModel
from typing import List
import json
import requests

class RDFClass(BaseModel):
    label: str
    uri: str

class SubjectClinicalData(BaseModel):
    collection: str
    patient_id: str
    disease_type: str = None
    location: str
    sexlabel: str = None
    age: int = None
    stagelabel: str = None

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
            if var in row.keys():
                new_row[var] = row[var]['value']
        ret.append(new_row)
    return ret

app = FastAPI()

@app.get("/", response_model=List[SubjectClinicalData])
def query_all_clinical_data(collection: str = None,
                            disease_type: str = None,
                            location: str = None,
                            sexlabel: str = None):
    """This is the main endpoint to query all of the loaded clinical data.

    As we add additional fields there will be additional parameters that will allow filtering."""
    query = """PREFIX collection: <http://purl.org/PRISM_0000001>
PREFIX subject_id: <http://purl.org/PRISM_0000002>
PREFIX diseasestage: <http://purl.obolibrary.org/obo/NCIT_C28108>
PREFIX diseasedisorderfinding: <http://purl.obolibrary.org/obo/NCIT_C7057>
PREFIX about: <http://purl.obolibrary.org/obo/IAO_0000136>
PREFIX age: <http://purl.obolibrary.org/obo/PATO_0000011>
PREFIX malesex: <http://purl.obolibrary.org/obo/PATO_0000384>
PREFIX femalesex: <http://purl.obolibrary.org/obo/PATO_0000383>
PREFIX phensex: <http://purl.obolibrary.org/obo/PATO_0001894>
PREFIX inheres: <http://purl.obolibrary.org/obo/RO_0000052>
PREFIX human: <http://purl.obolibrary.org/obo/NCBITaxon_9606>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX identifier: <http://purl.obolibrary.org/obo/IAO_0020000>
PREFIX denotes: <http://purl.obolibrary.org/obo/IAO_0000219>
PREFIX has_part: <http://purl.obolibrary.org/obo/BFO_0000051>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
select distinct ?collection ?patient_id ?sexlabel ?age ?location ?disease_type ?stagelabel{

    # the subject identifier
    ?id denotes: ?person .
    ?id rdf:type subject_id: .
    ?id rdfs:label ?patient_id .

    # collection, collection name
    ?c rdf:type collection: .
    ?c rdfs:label ?collection .

    # collections have subject ids as parts
    ?c has_part: ?id .
    ?id rdf:type subject_id: .
    ?id rdfs:label ?patient_id .

    optional{
        # the person's sex
        ?sex inheres: ?person .
        ?sex rdf:type ?sexclass .
        ?sexclass rdfs:subClassOf phensex: .
        ?sexclass rdfs:label ?sexlabel .
    }

    optional{
        # the person's age
        ?ag inheres: ?person .
        ?ag rdf:type age: .
        ?ag rdfs:label ?age .
    }

    optional{
        # parts of this person
        ?person has_part: ?ppart .
        ?ppart rdf:type ?loctype .
        ?loctype rdfs:label ?location .
        # want only the immediate location type -- not superclasses like 'organ subunit'
        FILTER NOT EXISTS{
            ?ppart rdf:type ?x .
            ?x rdfs:subClassOf ?loctype.
            filter (?x != ?loctype)
        }
    }

    optional{
        # the disease in this part of the person
        ?dis_inst inheres: ?ppart .
        ?dis_inst rdf:type ?dt .
        ?dt rdfs:subClassOf diseasedisorderfinding: .
        ?dt rdfs:label ?disease_type .
        # want only the immediate diease type
        FILTER NOT EXISTS{
            ?dis_inst rdf:type ?x .
            ?x rdfs:subClassOf ?dt
            filter (?x != ?dt)
        }

        ?stage_inst rdf:type ?stage_class .
        ?stage_inst about: ?dis_inst .
        ?stage_class rdfs:subClassOf diseasestage: .
        ?stage_class rdfs:label ?stagelabel .
        FILTER NOT EXISTS{
            ?stage_inst rdf:type ?x .
            ?x rdfs:subClassOf ?stage_class .
            filter (?x != ?stage_class)
        }
    }
}"""
    ret = make_sparql_query(query)
    if collection is not None:
        filter = []
        for row in ret:
            if(row['collection'] == collection):
                filter.append(row)
        ret = filter
    if disease_type is not None:
        filter = []
        for row in ret:
            if(row.get('disease_type') == disease_type):
                filter.append(row)
        ret = filter
    if location is not None:
        filter = []
        for row in ret:
            if(row['location'] == location):
                filter.append(row)
        ret = filter
    if sexlabel is not None:
        filter = []
        for row in ret:
            if(row.get('sexlabel') == sexlabel):
                filter.append(row)
        ret = filter
    return ret

@app.get("/locations", response_model=List[RDFClass])
def list_all_locations():
    """List all of the physical locations associated with clinical data."""
    query = """PREFIX human: <http://purl.obolibrary.org/obo/NCBITaxon_9606>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX identifier: <http://purl.obolibrary.org/obo/IAO_0020000>
PREFIX has_part: <http://purl.obolibrary.org/obo/BFO_0000051>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
select distinct ?label ?uri {
	# the person
	?person rdf:type human: .
    # parts of this person
 	?person has_part: ?lt .
    ?lt rdf:type ?uri .
    ?uri rdfs:label ?label .
    # want only the immediate location type -- not superclasses like 'organ subunit'
    FILTER NOT EXISTS{
        ?x rdfs:subClassOf ?uri.
    }
}"""
    results = make_sparql_query(query)
    return results

@app.get("/disease_types", response_model=List[RDFClass])
def list_all_disease_types():
    """List all of the disease types avaliable in the clinical data."""
    query = """PREFIX collection: <http://purl.org/PRISM_0000001>
PREFIX inheres: <http://purl.obolibrary.org/obo/RO_0000052>
PREFIX human: <http://purl.obolibrary.org/obo/NCBITaxon_9606>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX has_part: <http://purl.obolibrary.org/obo/BFO_0000051>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
select distinct ?label ?uri {
	# the person
	?person rdf:type human: .
    ?dis_inst inheres: ?ppart .
    ?dis_inst rdf:type ?uri .
    ?uri rdfs:label ?label .
    # want only the immediate diease type
    FILTER NOT EXISTS{
        ?x rdfs:subClassOf ?uri .
    }
}"""
    return make_sparql_query(query)

@app.get("/collections")
def list_all_collections():
    """List all collections which currently have clinical data."""
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
