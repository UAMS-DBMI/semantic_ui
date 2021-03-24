PREFIX = """PREFIX collection: <http://purl.org/PRISM#PRISM_0000001>
PREFIX subject_id: <http://purl.org/PRISM#PRISM_0000002>
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
PREFIX age_assay: <http://purl.obolibrary.org/obo/OBI_0001158>
PREFIX age_datum: <http://purl.obolibrary.org/obo/OBI_0001167>
PREFIX has_spec_output: <http://purl.obolibrary.org/obo/OBI_0000299>
PREFIX has_value_spec: <http://purl.obolibrary.org/obo/OBI_0001938>
PREFIX has_spec_value: <http://purl.obolibrary.org/obo/OBI_0002135>
PREFIX has_meas_unit_label: <http://purl.obolibrary.org/obo/IAO_0000039>
PREFIX evaluant_role: <http://purl.obolibrary.org/obo/OBI_0000067>
PREFIX realizes: <http://purl.obolibrary.org/obo/BFO_0000055>
"""

PATIENT = """
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
"""

# the person's sex
SEX = """
?sex inheres: ?person .
?sex rdf:type ?sexclass .
?sexclass rdfs:subClassOf phensex: .
?sexclass rdfs:label ?sexlabel .
"""

# the person's age
AGE = """
?amd rdf:type age_datum: .
?amd about: ?person .
?amd has_value_spec: ?vspec .
?vspec has_spec_value: ?age .
"""

# parts of this person
LOCATION = """
?person has_part: ?ppart .
?ppart rdf:type ?loctype .
?loctype rdfs:label ?location .
"""

# the disease in this part of the person
DISEASE = """
?dis_inst inheres: ?ppart .
?dis_inst rdf:type ?dt .
?dt rdfs:subClassOf diseasedisorderfinding: .
?dt rdfs:label ?disease_type .
"""

STAGE = """
?stage_inst rdf:type ?stage_class .
?stage_inst about: ?dis_inst .
?stage_class rdfs:subClassOf diseasestage: .
?stage_class rdfs:label ?stagelabel .
"""

def all_from_patient_ids(patient_ids):
    formatted_ids = ["'{}'".format(x) for x in patient_ids]
    filter_line = "values ?patient_id {{{}}} .".format(' '.join(formatted_ids))
    query = f"""{PREFIX}
    select distinct ?collection ?patient_id ?sexlabel ?age ?location ?disease_type ?stagelabel {{
        {filter_line}
        {PATIENT}
        optional{{
            {SEX}
        }}
        optional{{
            {AGE}
        }}
        optional{{
            {LOCATION}
            # want only the immediate location type -- not superclasses like 'organ subunit'
            FILTER NOT EXISTS{{
                ?ppart rdf:type ?x .
                ?x rdfs:subClassOf ?loctype.
                filter (?x != ?loctype)
            }}
        }}
        optional{{
            {DISEASE}
            # want only the immediate diease type
            FILTER NOT EXISTS{{
                ?dis_inst rdf:type ?x .
                ?x rdfs:subClassOf ?dt
                filter (?x != ?dt)
            }}
        }}
        optional{{
            {STAGE}
            # want only the immediate stage type
            FILTER NOT EXISTS{{
                ?stage_inst rdf:type ?x .
                ?x rdfs:subClassOf ?stage_class .
                filter (?x != ?stage_class)
            }}
        }}
    }}"""
    return query

def ids_from_stage_uris(stage_uris):
    formatted_uris = ["<{}>".format(x) for x in stage_uris]
    long_string = ','.join(formatted_uris)
    filter_line = f"filter(?stage_class in ({long_string})) ."
    query = f"""{PREFIX}
    select distinct ?patient_id ?stage_class {{
        {PATIENT}
        {LOCATION}
        {DISEASE}
        {STAGE}
        {filter_line}
    }}"""
    return query


def ids_from_location_uris(location_uris):
    formatted_uris = ["<{}>".format(x) for x in location_uris]
    long_string = ','.join(formatted_uris)
    filter_line = f"filter(?loctype in ({long_string})) ."
    query = f"""{PREFIX}
    select distinct ?patient_id ?loctype {{
        {PATIENT}
        {LOCATION}
        {filter_line}
        {DISEASE}
    }}"""
    return query

def ids_from_sex_uris(sex_uris):
    formatted_uris = ["<{}>".format(x) for x in sex_uris]
    long_string = ','.join(formatted_uris)
    filter_line = f"filter(?sexclass in ({long_string})) ."
    query = f"""{PREFIX}
    select distinct ?patient_id ?sexclass {{
        {PATIENT}
        {SEX}
        {filter_line}
    }}"""
    return query

def ids_from_disease_uris(disease_uris):
    formatted_uris = ["<{}>".format(x) for x in disease_uris]
    long_string = ','.join(formatted_uris)
    filter_line = f"filter(?dt in ({long_string})) ."
    query = f"""{PREFIX}
    select distinct ?patient_id ?dt {{
        {PATIENT}
        {DISEASE}
        {LOCATION}
        {filter_line}
    }}"""
    return query

def all_age():
    query = f"""{PREFIX}
    select distinct ?patient_id ?age {{
        # the subject identifier
        {PATIENT}
        {AGE}
    }}"""
    return query

def collection_metadata():
    return """PREFIX collection: <http://purl.org/PRISM#PRISM_0000001>
PREFIX has_part: <http://purl.obolibrary.org/obo/BFO_0000051>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX description: <http://purl.org/dc/elements/1.1/description>
PREFIX data_item: <http://purl.obolibrary.org/obo/IAO_0000027>

select ?name ?link ?desc ?tl {
    ?c rdf:type collection: .
    ?c rdfs:label ?name .
    ?c rdfs:seeAlso ?link .
    ?c description: ?desc .
    ?c has_part: ?x .
    ?x rdf:type ?t .
    ?t rdfs:label ?tl .
    ?t rdfs:subClassOf data_item: .
} order by ?name"""

def collection_counts():
    return """PREFIX collection: <http://purl.org/PRISM#PRISM_0000001>
PREFIX subject_id: <http://purl.org/PRISM#PRISM_0000002>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX denotes: <http://purl.obolibrary.org/obo/IAO_0000219>
PREFIX has_part: <http://purl.obolibrary.org/obo/BFO_0000051>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
select ?collection (count(?patient_id) as ?patient_count) {

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

} group by ?collection"""

def labels_by_subclass(uri):
    return f"""PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    select distinct ?value ?label ?definition where {{
        ?value rdfs:subClassOf <{uri}> .
        ?part sesame:directType ?value .
        ?value rdfs:label ?label .
        optional {{ ?value <http://purl.obolibrary.org/obo/IAO_0000115> ?definition . }}
    }} order by ?label"""

if __name__ == '__main__':
    import requests
    def _make_sparql_query(query, triplestore_url):
        payload = {'query': query}
        headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Accept': 'application/sparql-results+json'}
        r = requests.post(triplestore_url, data=payload, headers=headers)
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
    triplestore_url = 'http://localhost:7200/repositories/prism'
    patient_ids = ['C3L-02219', 'C3N-02451', 'C3L-00016', 'BreastDX-01-0038']
    query = all_from_patient_ids(patient_ids)
    print(query)
    print(f"all {len(_make_sparql_query(query, triplestore_url))}")
    disease_uris = ['http://purl.obolibrary.org/obo/NCIT_C136709', 'http://purl.obolibrary.org/obo/NCIT_C4105']
    query = ids_from_disease_uris(disease_uris)
    print(f"disease {len(_make_sparql_query(query, triplestore_url))}")
    location_uris = ['http://purl.obolibrary.org/obo/UBERON_0001872', 'http://purl.obolibrary.org/obo/UBERON_0006518']
    query = ids_from_location_uris(location_uris)
    print(f"location {len(_make_sparql_query(query, triplestore_url))}")
    sex_uris = ['http://purl.obolibrary.org/obo/PATO_0000384']
    query = ids_from_sex_uris(sex_uris)
    print(f"sex {len(_make_sparql_query(query, triplestore_url))}")
    stage_uris = ['http://purl.obolibrary.org/obo/NCIT_C28054']
    query = ids_from_stage_uris(stage_uris)
    print(f"stage {len(_make_sparql_query(query, triplestore_url))}")
    query = all_age()
    print(f"ages {len(_make_sparql_query(query, triplestore_url))}")
    query = labels_by_subclass('http://purl.obolibrary.org/obo/UBERON_0001062')
    print(query)
    print(f"labels {len(_make_sparql_query(query, triplestore_url))}")
