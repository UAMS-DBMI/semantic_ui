def breast_query():
    return """
    PREFIX collection: <http://purl.org/PRISM#PRISM_0000001>
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

    select distinct ?patient_id ?id{

# the subject identifier
?id denotes: ?person .
?id rdf:type subject_id: .
?id rdfs:label ?patient_id .

# collection, collection name
?c rdf:type collection: .
?c rdfs:label ?collection .
?c rdfs:label "Breast-MRI-NACT-Pilot" .

# collections have subject ids as parts
?c has_part: ?id .
?id rdf:type subject_id: .
?id rdfs:label ?patient_id .
} order by ?patient_id
"""

def update_breast(uri, label):
    old_label = label
    new_label = label.replace('_', '-')
    return f"""PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
DELETE {{ <{uri}> rdfs:label '{old_label}' }}
INSERT {{ <{uri}> rdfs:label '{new_label}' }}
where {{ }}
    """

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
    triplestore_url = 'http://triplestore-prism.apps.dbmi.cloud/repositories/prism'
    query = breast_query()
    print(query)
    ret = _make_sparql_query(query, triplestore_url)
    for row in ret:
        query = update_breast(row['id'], row['patient_id'])
        payload = {'update': query}
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        r = requests.post(f"{triplestore_url}/statements", data=payload, headers=headers)
        r.raise_for_status()
