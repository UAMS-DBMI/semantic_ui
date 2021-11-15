#!/usr/bin/env python

from fastapi import FastAPI, HTTPException, Response
from collections import defaultdict
from pydantic import BaseModel
from typing import List
import json
import requests
import os
import random

TRIPLESTORE_URL = os.getenv('SEMAPI_TRIPLESTORE_URL', 'http://localhost:7200/repositories/prism')
config = []
with open('aries_config.json') as f:
    config = json.load(f)

data = []
with open('aries_raw_data.json') as f:
    data = json.load(f)

app = FastAPI()

@app.get("/config")
def get_config():
    return config

@app.get("/collections")
def get_collections():
    # query = queries.collection_metadata()
    # results = make_sparql_query(query)
    # query = queries.collection_counts()
    # count_results = make_sparql_query(query)
    # counts = {}
    # total_count = 0
    # for row in count_results:
    #     counts[row['collection']] = row['patient_count']
    #     total_count += int(row['patient_count'])
    # all_features = []
    # ret = []
    # last_col = ''
    # cur_col = {}
    # for row in results:
    #     if row['tl'] not in all_features:
    #         all_features.append(row['tl'])
    #     if row['name'] != last_col:
    #         if last_col != '':
    #             ret.append(cur_col)
    #         cur_col = {'name': row['name'],
    #                    'link': row['link'],
    #                    'desc': row['desc'],
    #                    'count': counts[row['name']],
    #                    'features': [row['tl']]}
    #         last_col = row['name']
    #     else:
    #         cur_col['features'].append(row['tl'])
    # ret.append(cur_col)
    return {'total': len(data), 'features': [], 'collections': [{}]}

@app.get("/data/raw-checkbox")
def get_raw_checkbox(name: str, uris: str = None):
    choices = uris.split(',')
    ret = defaultdict(list)
    for id, d in data.items():
        for choice in choices:
            if(d[f"{name}___{choice}"] == 'Checked'):
                ret[choice].append(id)
    return ret

@app.get("/data/raw-radio")
def get_raw_radio(name: str, uris: str = None):
    choices = uris.split(',')
    ret = defaultdict(list)
    for id, d in data.items():
        for choice in choices:
            if(d[name] == choice):
                ret[choice].append(id)
    return ret

@app.get("/data/raw-dropdown")
def get_raw_dropdown(name: str, uris: str = None):
    choices = uris.split(',')
    ret = defaultdict(list)
    for id, d in data.items():
        for choice in choices:
            if(d[name] == choice):
                ret[choice].append(id)
    return ret

@app.get('/data/raw-calc')
def get_raw_calc(name: str, min: int = None, max: int = None):
    ret = defaultdict(list)
    for id, d in data.items():
        val = float(d[name])
        if((min is None or val > min) and (max is None or val < max)):
            ret[val].append(id)
    return ret

@app.get("/data")
def get_all_data(patient_ids: str = None, downloadFile: str = None):
    ids = patient_ids.split(',')
    results = []
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
    random_count = 10
    if(len(patient_ids.patient_ids) < random_count):
        random_count = len(patient_ids.patient_ids)
    ids = random.sample(patient_ids.patient_ids, random_count)
    return []
