#!/usr/bin/env python

from fastapi import FastAPI, HTTPException, Response
from collections import defaultdict
from pydantic import BaseModel
from typing import List
import json
import requests
import os

TRIPLESTORE_URL = os.getenv('SEMAPI_TRIPLESTORE_URL', 'http://localhost:7200/repositories/prism')

class RDFClass(BaseModel):
    label: str
    uri: str

class SubjectClinicalData(BaseModel):
    collection: str
    patient_id: str
    disease_type: str = None
    location: str = None
    sexlabel: str = None
    age: int = None
    stagelabel: str = None

def make_sparql_query(query, params={}):
    payload = {'query': query}
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Accept': 'application/sparql-results+json'}
    r = requests.post(TRIPLESTORE_URL, data=payload, headers=headers)
    r.raise_for_status()
    ret = []
    results = r.json()
    vars = results['head']['vars']
    for row in results['results']['bindings']:
        new_row = {}
        for var in vars:
            if var in row.keys():
                new_row[var] = row[var]['value']
        ret.append(new_row)
    return ret

def make_data_table_query(query, params={}):
    data = {'query': query}
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Accept': 'application/sparql-results+json'}
    r = requests.post(TRIPLESTORE_URL, data=data, headers=headers)
    r.raise_for_status()
    results = r.json()
    ret = {}
    rows = []
    ret['columns'] = results['head']['vars']
    for row in results['results']['bindings']:
        new_row = []
        for var in ret['columns']:
            if var in row.keys():
                new_row.append(row[var]['value'])
            else:
                new_row.append(None)
        rows.append(new_row)
    ret['data'] = rows
    return ret

app = FastAPI()

@app.get("/api", response_model=List[SubjectClinicalData])
def query_all_clinical_data(collection: str = None,
                            disease: str = None,
                            location: str = None,
                            stage: str = None,
                            sex: str = None):
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
    if disease is not None:
        filter = []
        for row in ret:
            if(row.get('disease_type') == disease):
                filter.append(row)
        ret = filter
    if stage is not None:
        filter = []
        for row in ret:
            if(row.get('stagelabel') == stage):
                filter.append(row)
        ret = filter
    if location is not None:
        filter = []
        for row in ret:
            if(row['location'] == location):
                filter.append(row)
        ret = filter
    if sex is not None:
        filter = []
        for row in ret:
            if(row.get('sexlabel') == sex):
                filter.append(row)
        ret = filter
    return ret

class Options(BaseModel):
    label: str = None
    type: str

@app.get("/select_box", response_model=List[Options])
def get_select_box():
    """This is an endpoint to populate the select box for the PRISM search interface."""

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
    collections = set()
    disease_types = set()
    locations = set()
    stagelabels = set()
    for row in ret:
        if(row.get('collection')):
            collections.add(row.get('collection'))
        if(row.get('disease_type')):
            disease_types.add(row.get('disease_type'))
        if(row.get('location')):
            locations.add(row.get('location'))
        if(row.get('stagelabel')):
            stagelabels.add(row.get('stagelabel'))
    options = []
    for collection in collections:
        options.append({'label': collection, 'type': 'Collection'})
    for disease_type in disease_types:
        options.append({'label': disease_type, 'type': 'Disease'})
    for location in locations:
        options.append({'label': location, 'type': 'Location'})
    for stagelabel in stagelabels:
        options.append({'label': stagelabel, 'type': 'Stage'})
    options.append({'label': 'male', 'type': 'Sex'})
    options.append({'label': 'female', 'type': 'Sex'})
    return options


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

@app.get("/age")
def get_age_data(min: int = None, max: int = None):
    """Retreive all patient ids for an age range."""
    query = """PREFIX subject_id: <http://purl.org/PRISM_0000002>
PREFIX age: <http://purl.obolibrary.org/obo/PATO_0000011>
PREFIX inheres: <http://purl.obolibrary.org/obo/RO_0000052>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX identifier: <http://purl.obolibrary.org/obo/IAO_0020000>
PREFIX denotes: <http://purl.obolibrary.org/obo/IAO_0000219>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
select distinct ?patient_id ?age {

    # the subject identifier
    ?id denotes: ?person .
    ?id rdf:type subject_id: .
    ?id rdfs:label ?patient_id .

    # the person's age
    ?ag inheres: ?person .
    ?ag rdf:type age: .
    ?ag rdfs:label ?age .
}"""
    results = make_sparql_query(query)
    result_set = defaultdict(list)
    for row in results:
        if (min == None or int(row['age']) >= min) and (max == None or int(row['age']) <= max):
            result_set[row['age']].append(row['patient_id'])
    return result_set

@app.get("/data/disease")
def get_disease_data(uris: str = None):
    valid_uris = uris.split(',')
    formatted_uris = ["<{}>".format(x) for x in valid_uris]
    filter_line = "filter(?dt in ({})) .".format(','.join(formatted_uris))
    """Retreive all patient ids for disease types."""
    query = """PREFIX subject_id: <http://purl.org/PRISM_0000002>
PREFIX diseasedisorderfinding: <http://purl.obolibrary.org/obo/NCIT_C7057>
PREFIX about: <http://purl.obolibrary.org/obo/IAO_0000136>
PREFIX inheres: <http://purl.obolibrary.org/obo/RO_0000052>
PREFIX human: <http://purl.obolibrary.org/obo/NCBITaxon_9606>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX denotes: <http://purl.obolibrary.org/obo/IAO_0000219>
PREFIX has_part: <http://purl.obolibrary.org/obo/BFO_0000051>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
select distinct ?patient_id ?dt {

    # the subject identifier
    ?id denotes: ?person .
    ?id rdf:type subject_id: .
    ?id rdfs:label ?patient_id .

    ?person has_part: ?ppart .
    ?ppart rdf:type ?loctype .
    ?loctype rdfs:label ?location .

    # the disease in this part of the person
    ?dis_inst inheres: ?ppart .
    ?dis_inst rdf:type ?dt .
    ?dt rdfs:subClassOf diseasedisorderfinding: .
    ?dt rdfs:label ?disease_type .
    %s
}""" % (filter_line)
    results = make_sparql_query(query)
    result_set = defaultdict(list)
    for row in results:
        result_set[row['dt']].append(row['patient_id'])
    return result_set

@app.get("/data/sex")
def get_sex_data(uris: str = None):
    valid_uris = uris.split(',')
    formatted_uris = ["<{}>".format(x) for x in valid_uris]
    filter_line = "filter(?sexclass in ({})) .".format(','.join(formatted_uris))
    """Retreive all patient ids for disease types."""
    query = """PREFIX collection: <http://purl.org/PRISM_0000001>
PREFIX subject_id: <http://purl.org/PRISM_0000002>
PREFIX about: <http://purl.obolibrary.org/obo/IAO_0000136>
PREFIX phensex: <http://purl.obolibrary.org/obo/PATO_0001894>
PREFIX inheres: <http://purl.obolibrary.org/obo/RO_0000052>
PREFIX human: <http://purl.obolibrary.org/obo/NCBITaxon_9606>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX identifier: <http://purl.obolibrary.org/obo/IAO_0020000>
PREFIX denotes: <http://purl.obolibrary.org/obo/IAO_0000219>
PREFIX has_part: <http://purl.obolibrary.org/obo/BFO_0000051>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
select distinct ?patient_id ?sexclass{

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

    # the person's sex
    ?sex inheres: ?person .
    ?sex rdf:type ?sexclass .
    ?sexclass rdfs:subClassOf phensex: .
    %s
}""" % (filter_line)
    results = make_sparql_query(query)
    result_set = defaultdict(list)
    for row in results:
        result_set[row['sexclass']].append(row['patient_id'])
    return result_set

@app.get("/data/location")
def get_location_data(uris: str = None):
    valid_uris = uris.split(',')
    formatted_uris = ["<{}>".format(x) for x in valid_uris]
    filter_line = "filter(?loctype in ({})) .".format(','.join(formatted_uris))
    """Retreive all patient ids for disease types."""
    query = """PREFIX collection: <http://purl.org/PRISM_0000001>
PREFIX subject_id: <http://purl.org/PRISM_0000002>
PREFIX diseasedisorderfinding: <http://purl.obolibrary.org/obo/NCIT_C7057>
PREFIX about: <http://purl.obolibrary.org/obo/IAO_0000136>
PREFIX inheres: <http://purl.obolibrary.org/obo/RO_0000052>
PREFIX human: <http://purl.obolibrary.org/obo/NCBITaxon_9606>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX identifier: <http://purl.obolibrary.org/obo/IAO_0020000>
PREFIX denotes: <http://purl.obolibrary.org/obo/IAO_0000219>
PREFIX has_part: <http://purl.obolibrary.org/obo/BFO_0000051>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
select distinct ?patient_id ?loctype {

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

    # parts of this person
    ?person has_part: ?ppart .
    ?ppart rdf:type ?loctype .
    ?loctype rdfs:label ?location .
    %s

    # the disease in this part of the person
    ?dis_inst inheres: ?ppart .
    ?dis_inst rdf:type ?dt .
    ?dt rdfs:subClassOf diseasedisorderfinding: .
    ?dt rdfs:label ?disease_type .
}""" % (filter_line)
    results = make_sparql_query(query)
    result_set = defaultdict(list)
    for row in results:
        result_set[row['loctype']].append(row['patient_id'])
    return result_set

@app.get("/data/stage")
def get_stage_data(uris: str = None):
    valid_uris = uris.split(',')
    formatted_uris = ["<{}>".format(x) for x in valid_uris]
    filter_line = "filter(?stage_class in ({})) .".format(','.join(formatted_uris))
    """Retreive all patient ids for disease types."""
    query = """PREFIX collection: <http://purl.org/PRISM_0000001>
PREFIX subject_id: <http://purl.org/PRISM_0000002>
PREFIX diseasestage: <http://purl.obolibrary.org/obo/NCIT_C28108>
PREFIX diseasedisorderfinding: <http://purl.obolibrary.org/obo/NCIT_C7057>
PREFIX about: <http://purl.obolibrary.org/obo/IAO_0000136>
PREFIX inheres: <http://purl.obolibrary.org/obo/RO_0000052>
PREFIX human: <http://purl.obolibrary.org/obo/NCBITaxon_9606>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX identifier: <http://purl.obolibrary.org/obo/IAO_0020000>
PREFIX denotes: <http://purl.obolibrary.org/obo/IAO_0000219>
PREFIX has_part: <http://purl.obolibrary.org/obo/BFO_0000051>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
select distinct ?patient_id ?stage_class{

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

    # parts of this person
    ?person has_part: ?ppart .
    ?ppart rdf:type ?loctype .
    ?loctype rdfs:label ?location .

    # the disease in this part of the person
    ?dis_inst inheres: ?ppart .
    ?dis_inst rdf:type ?dt .
    ?dt rdfs:subClassOf diseasedisorderfinding: .
    ?dt rdfs:label ?disease_type .

    ?stage_inst rdf:type ?stage_class .
    ?stage_inst about: ?dis_inst .
    ?stage_class rdfs:subClassOf diseasestage: .
    ?stage_class rdfs:label ?stagelabel .
    %s
}""" % (filter_line)
    results = make_sparql_query(query)
    result_set = defaultdict(list)
    for row in results:
        result_set[row['stage_class']].append(row['patient_id'])
    return result_set

@app.get("/data")
def get_all_data(patient_ids: str = None, downloadFile: str = None):
    ids = patient_ids.split(',')
    formatted_ids = ["'{}'".format(x) for x in ids]
    filter_line = "filter(?patient_id in ({})) .".format(','.join(formatted_ids))
    """Retreive all patient ids for disease types."""
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
    %s

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
}""" % (filter_line)
    results = make_data_table_query(query)
    if downloadFile is None:
        return results
    else:
        bigstr = ','.join(results['columns']) + '\n'
        for row in results['data']:
            bigstr += ','.join(row) + '\n'
        headers = {'Content-Disposition': 'attachment; filename={}.csv'.format(downloadFile)}
        return Response(content=bigstr, headers=headers, media_type='text/csv')
