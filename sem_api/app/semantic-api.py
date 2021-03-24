#!/usr/bin/env python

from fastapi import FastAPI, HTTPException, Response
from collections import defaultdict
from pydantic import BaseModel
from typing import List
import json
import requests
import os
import queries as queries

TRIPLESTORE_URL = os.getenv('SEMAPI_TRIPLESTORE_URL', 'http://localhost:7200/repositories/prism')


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
                new_row.append('')
        rows.append(new_row)
    ret['data'] = rows
    return ret

app = FastAPI()

@app.get("/config")
def get_config():
    config = [
      {
        "choices": [
          {
            "value": "http://purl.obolibrary.org/obo/PATO_0000384",
            "label": "Male"
          },
          {
            "value": "http://purl.obolibrary.org/obo/PATO_0000383",
            "label": "Female"
          }
        ],
        "type": "radio",
        "api": "sex",
        "name": "Biological Sex",
        "label": "Sex"
      },
      {
        "type": "calc",
        "api": "age",
        "name": "Age in Years",
        "label": "Age"
      }
    ]

    # lung located diseases
    query = queries.labels_by_subclass('http://purl.obolibrary.org/obo/NCIT_C27669')
    lung_opts = make_sparql_query(query)
    config.append({
        'type': 'radio',
        'api': 'disease',
        'name': 'Lung Diseases',
        'label': 'Diseases located in the lung.',
        'choices': lung_opts
    })

    # brain located diseases
    query = queries.labels_by_subclass('http://purl.obolibrary.org/obo/NCIT_C26835')
    brain_opts = make_sparql_query(query)
    config.append({
        'type': 'radio',
        'api': 'disease',
        'name': 'Brain Diseases',
        'label': 'Diseases located in the brain.',
        'choices': brain_opts
    })

    # breast located diseases
    query = queries.labels_by_subclass('http://purl.obolibrary.org/obo/NCIT_C26709')
    breast_opts = make_sparql_query(query)
    config.append({
        'type': 'radio',
        'api': 'disease',
        'name': 'Breast Diseases',
        'label': 'Diseases located in the breast.',
        'choices': breast_opts
    })

    # stage information
    query = queries.labels_by_subclass('http://purl.obolibrary.org/obo/NCIT_C28108')
    stage_opts = make_sparql_query(query)
    config.append({
        "type": "radio",
        "api": "stage",
        "name": "Cancer Stage",
        "label": "The extent of a cancer in the body. Staging is usually based on the size of the tumor, whether lymph nodes contain cancer, and whether the cancer has spread from the original site to other parts of the body.",
        "choices": stage_opts
    })

    # locations
    query = queries.labels_by_subclass('http://purl.obolibrary.org/obo/UBERON_0001062')
    location_opts = make_sparql_query(query)
    config.append({
        "type": "radio",
        "name": "Location",
        "api": "location",
        "label": "The primary location of the disease.",
        "choices": location_opts
    })

    # brain locations
    query = queries.labels_by_subclass('http://purl.obolibrary.org/obo/UBERON_0016526')
    location_opts = make_sparql_query(query)
    config.append({
        "type": "radio",
        "name": "Brain Lobes",
        "api": "location",
        "label": "The primary location of the disease.",
        "choices": location_opts
    })
    return config

@app.get("/collections")
def get_collections():
    query = queries.collection_metadata()
    results = make_sparql_query(query)
    query = queries.collection_counts()
    count_results = make_sparql_query(query)
    counts = {}
    total_count = 0
    for row in count_results:
        counts[row['collection']] = row['patient_count']
        total_count += int(row['patient_count'])
    all_features = []
    ret = []
    last_col = ''
    cur_col = {}
    for row in results:
        if row['tl'] not in all_features:
            all_features.append(row['tl'])
        if row['name'] != last_col:
            if last_col != '':
                ret.append(cur_col)
            cur_col = {'name': row['name'],
                       'link': row['link'],
                       'desc': row['desc'],
                       'count': counts[row['name']],
                       'features': [row['tl']]}
            last_col = row['name']
        else:
            cur_col['features'].append(row['tl'])
    ret.append(cur_col)
    return {'total': total_count, 'features': all_features, 'collections': ret}

@app.get("/data/disease")
def get_disease_data(uris: str = None):
    valid_uris = uris.split(',')
    query = queries.ids_from_disease_uris(valid_uris)
    results = make_sparql_query(query)
    result_set = defaultdict(list)
    for row in results:
        result_set[row['dt']].append(row['patient_id'])
    return result_set

@app.get("/data/sex")
def get_sex_data(uris: str = None):
    valid_uris = uris.split(',')
    query = queries.ids_from_sex_uris(valid_uris)
    results = make_sparql_query(query)
    result_set = defaultdict(list)
    for row in results:
        result_set[row['sexclass']].append(row['patient_id'])
    return result_set

@app.get("/data/location")
def get_location_data(uris: str = None):
    valid_uris = uris.split(',')
    query = queries.ids_from_location_uris(valid_uris)
    results = make_sparql_query(query)
    result_set = defaultdict(list)
    for row in results:
        result_set[row['loctype']].append(row['patient_id'])
    return result_set

@app.get("/data/stage")
def get_stage_data(uris: str = None):
    valid_uris = uris.split(',')
    query = queries.ids_from_stage_uris(valid_uris)
    results = make_sparql_query(query)
    result_set = defaultdict(list)
    for row in results:
        result_set[row['stage_class']].append(row['patient_id'])
    return result_set

@app.get("/data")
def get_all_data(patient_ids: str = None, downloadFile: str = None):
    ids = patient_ids.split(',')
    query = queries.all_from_patient_ids(ids)
    results = make_data_table_query(query)
    if downloadFile is None:
        return results
    else:
        bigstr = ','.join(results['columns']) + '\n'
        for row in results['data']:
            bigstr += ','.join(row) + '\n'
        headers = {'Content-Disposition': 'attachment; filename={}.csv'.format(downloadFile)}
        return Response(content=bigstr, headers=headers, media_type='text/csv')

class PIDS(BaseModel):
    patient_ids: List[str]

@app.post("/data")
def post_all_data(patient_ids: PIDS):
    query = queries.all_from_patient_ids(patient_ids.patient_ids)
    results = make_data_table_query(query)
    return results

@app.get("/age")
def get_age_data(min: int = None, max: int = None):
    query = queries.all_age()
    results = make_sparql_query(query)
    result_set = defaultdict(list)
    for row in results:
        if (min == None or int(row['age']) >= min) and (max == None or int(row['age']) <= max):
            result_set[row['age']].append(row['patient_id'])
    return result_set
