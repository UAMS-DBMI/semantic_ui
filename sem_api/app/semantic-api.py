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
        "type": "radio",
        "name": "disease",
        "choices": [
          {
            "value": "http://purl.obolibrary.org/obo/NCIT_C3768",
            "label": "Acinar Cell Carcinoma"
          },
          {
            "value": "http://purl.obolibrary.org/obo/NCIT_C7267",
            "label": "Combined Lung Large Cell Neuroendocrine Carcinoma"
          },
          {
            "value": "http://purl.obolibrary.org/obo/NCIT_C136709",
            "label": "Invasive Lung Mucinous Adenocarcinoma"
          },
          {
            "value": "http://purl.obolibrary.org/obo/NCIT_C4105",
            "label": "Keratinizing Squamous Cell Carcinoma"
          },
          {
            "value": "http://purl.obolibrary.org/obo/NCIT_C123160",
            "label": "Lepidic Predominant Adenocarcinoma"
          },
          {
            "value": "http://purl.obolibrary.org/obo/NCIT_C3512",
            "label": "Lung Adenocarcinoma"
          },
          {
            "value": "http://purl.obolibrary.org/obo/NCIT_C45507",
            "label": "Lung Basaloid Squamous Cell  Carcinoma"
          },
          {
            "value": "http://purl.obolibrary.org/obo/NCIT_C136710",
            "label": "Lung Enteric Adenocarcinoma"
          },
          {
            "value": "http://purl.obolibrary.org/obo/NCIT_C4450",
            "label": "Lung Large Cell Carcinoma"
          },
          {
            "value": "http://purl.obolibrary.org/obo/NCIT_C128847",
            "label": "Lung Micropapillary Adenocarcinoma"
          },
          {
            "value": "http://purl.obolibrary.org/obo/NCIT_C136714",
            "label": "Lung Non-Keratinizing Squamous Cell Carcinoma"
          },
          {
            "value": "http://purl.obolibrary.org/obo/NCIT_C2926",
            "label": "Lung Non-Small Cell Carcinoma"
          },
          {
            "value": "http://purl.obolibrary.org/obo/NCIT_C2923",
            "label": "Minimally Invasive Lung Adenocarcinoma"
          },
          {
            "value": "http://purl.obolibrary.org/obo/NCIT_C7268",
            "label": "Minimally Invasive Lung Mucinous Adenocarcinoma"
          },
          {
            "value": "http://purl.obolibrary.org/obo/NCIT_C26712",
            "label": "Mucinous Adenocarcinoma"
          },
          {
            "value": "http://purl.obolibrary.org/obo/NCIT_C2853",
            "label": "Papillary Adenocarcinoma"
          },
          {
            "value": "http://purl.obolibrary.org/obo/NCIT_C5651",
            "label": "Solid Lung Adenocarcinoma"
          },
          {
            "value": "http://purl.obolibrary.org/obo/NCIT_C2929",
            "label": "Squamous Cell Carcinoma"
          }
        ],
        "label": "The type of disease indicated in the clinical notes."
      },
      {
        "choices": [
          {
            "label": "right lung lobe",
            "value": "http://purl.obolibrary.org/obo/UBERON_0006518"
          },
          {
            "label": "left lung lobe",
            "value": "http://purl.obolibrary.org/obo/UBERON_0008951"
          },
          {
            "label": "middle lobe of right lung",
            "value": "http://purl.obolibrary.org/obo/UBERON_0002174",
            "indention": 1
          },
          {
            "label": "upper lobe of left lung",
            "value": "http://purl.obolibrary.org/obo/UBERON_0008952"
          },
          {
            "label": "lower lobe of right lung",
            "value": "http://purl.obolibrary.org/obo/UBERON_0002171"
          },
          {
            "label": "upper lobe of right lung",
            "value": "http://purl.obolibrary.org/obo/UBERON_0002170"
          },
          {
            "label": "lower lobe of left lung",
            "value": "http://purl.obolibrary.org/obo/UBERON_0008953"
          },
          {
            "label": "left lung hilus",
            "value": "http://purl.obolibrary.org/obo/UBERON_0004887"
          }
        ],
        "type": "radio",
        "name": "location",
        "label": "The primary location of the disease."
      },
      {
        "choices":[
          {
            "value": "http://purl.obolibrary.org/obo/NCIT_C27966",
            "label": "Stage I"
          },{
            "value": "http://purl.obolibrary.org/obo/NCIT_C27975",
            "label": "Stage IA"
          },{
            "value": "http://purl.obolibrary.org/obo/NCIT_C136485",
            "label": "Stage IA3"
          },{
            "value": "http://purl.obolibrary.org/obo/NCIT_C27976",
            "label": "Stage IB"
          },{
            "value": "http://purl.obolibrary.org/obo/NCIT_C28054",
            "label": "Stage II"
          },{
            "value": "http://purl.obolibrary.org/obo/NCIT_C27967",
            "label": "Stage IIA"
          },{
            "value": "http://purl.obolibrary.org/obo/NCIT_C27968",
            "label": "Stage IIB"
          },{
            "value": "http://purl.obolibrary.org/obo/NCIT_C27978",
            "label": "Stage IIIB"
          },{
            "value": "http://purl.obolibrary.org/obo/NCIT_C27971",
            "label": "Stage IV"
          }
        ],
        "type": "radio",
        "name": "stage",
        "label": "The extent of a cancer in the body. Staging is usually based on the size of the tumor, whether lymph nodes contain cancer, and whether the cancer has spread from the original site to other parts of the body."
      },
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
        "name": "sex",
        "label": "Sex"
      },
      {
        "type": "calc",
        "name": "age",
        "label": "Age"
      }
    ]
    return config

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
