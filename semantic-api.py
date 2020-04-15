#!/usr/bin/env python

from fastapi import FastAPI
from collections import defaultdict
import json

app = FastAPI()
data = []
with open('demo.json') as json_file:
    data = json.load(json_file)

@app.get("/demo")
def demo():
    return data

@app.get("/stats")
def stat_list():
    resp = []
    for item in data:
        for key in item.keys():
            if key not in resp:
                resp.append(key)
    return resp

@app.get("/stats/{stat_name}")
def stats(stat_name: str):
    resp = defaultdict(int)
    for item in data:
        if stat_name in item.keys():
            resp[item[stat_name]] += 1
    return resp
