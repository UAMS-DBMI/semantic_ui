import json

big_json = """
{
  "head": {
    "vars": [
      "disease_type",
      "dt"
    ]
  },
  "results": {
    "bindings": [
      {
        "dt": {
          "type": "uri",
          "value": "http://purl.obolibrary.org/obo/NCIT_C3768"
        },
        "disease_type": {
          "type": "literal",
          "value": "Acinar Cell Carcinoma"
        }
      },
      {
        "dt": {
          "type": "uri",
          "value": "http://purl.obolibrary.org/obo/NCIT_C7267"
        },
        "disease_type": {
          "type": "literal",
          "value": "Combined Lung Large Cell Neuroendocrine Carcinoma"
        }
      },
      {
        "dt": {
          "type": "uri",
          "value": "http://purl.obolibrary.org/obo/NCIT_C136709"
        },
        "disease_type": {
          "type": "literal",
          "value": "Invasive Lung Mucinous Adenocarcinoma"
        }
      },
      {
        "dt": {
          "type": "uri",
          "value": "http://purl.obolibrary.org/obo/NCIT_C4105"
        },
        "disease_type": {
          "type": "literal",
          "value": "Keratinizing Squamous Cell Carcinoma"
        }
      },
      {
        "dt": {
          "type": "uri",
          "value": "http://purl.obolibrary.org/obo/NCIT_C123160"
        },
        "disease_type": {
          "type": "literal",
          "value": "Lepidic Predominant Adenocarcinoma"
        }
      },
      {
        "dt": {
          "type": "uri",
          "value": "http://purl.obolibrary.org/obo/NCIT_C3512"
        },
        "disease_type": {
          "type": "literal",
          "value": "Lung Adenocarcinoma"
        }
      },
      {
        "dt": {
          "type": "uri",
          "value": "http://purl.obolibrary.org/obo/NCIT_C45507"
        },
        "disease_type": {
          "type": "literal",
          "value": "Lung Basaloid Squamous Cell  Carcinoma"
        }
      },
      {
        "dt": {
          "type": "uri",
          "value": "http://purl.obolibrary.org/obo/NCIT_C136710"
        },
        "disease_type": {
          "type": "literal",
          "value": "Lung Enteric Adenocarcinoma"
        }
      },
      {
        "dt": {
          "type": "uri",
          "value": "http://purl.obolibrary.org/obo/NCIT_C4450"
        },
        "disease_type": {
          "type": "literal",
          "value": "Lung Large Cell Carcinoma"
        }
      },
      {
        "dt": {
          "type": "uri",
          "value": "http://purl.obolibrary.org/obo/NCIT_C128847"
        },
        "disease_type": {
          "type": "literal",
          "value": "Lung Micropapillary Adenocarcinoma"
        }
      },
      {
        "dt": {
          "type": "uri",
          "value": "http://purl.obolibrary.org/obo/NCIT_C136714"
        },
        "disease_type": {
          "type": "literal",
          "value": "Lung Non-Keratinizing Squamous Cell Carcinoma"
        }
      },
      {
        "dt": {
          "type": "uri",
          "value": "http://purl.obolibrary.org/obo/NCIT_C2926"
        },
        "disease_type": {
          "type": "literal",
          "value": "Lung Non-Small Cell Carcinoma"
        }
      },
      {
        "dt": {
          "type": "uri",
          "value": "http://purl.obolibrary.org/obo/NCIT_C2923"
        },
        "disease_type": {
          "type": "literal",
          "value": "Minimally Invasive Lung Adenocarcinoma"
        }
      },
      {
        "dt": {
          "type": "uri",
          "value": "http://purl.obolibrary.org/obo/NCIT_C7268"
        },
        "disease_type": {
          "type": "literal",
          "value": "Minimally Invasive Lung Mucinous Adenocarcinoma"
        }
      },
      {
        "dt": {
          "type": "uri",
          "value": "http://purl.obolibrary.org/obo/NCIT_C26712"
        },
        "disease_type": {
          "type": "literal",
          "value": "Mucinous Adenocarcinoma"
        }
      },
      {
        "dt": {
          "type": "uri",
          "value": "http://purl.obolibrary.org/obo/NCIT_C2853"
        },
        "disease_type": {
          "type": "literal",
          "value": "Papillary Adenocarcinoma"
        }
      },
      {
        "dt": {
          "type": "uri",
          "value": "http://purl.obolibrary.org/obo/NCIT_C5651"
        },
        "disease_type": {
          "type": "literal",
          "value": "Solid Lung Adenocarcinoma"
        }
      },
      {
        "dt": {
          "type": "uri",
          "value": "http://purl.obolibrary.org/obo/NCIT_C2929"
        },
        "disease_type": {
          "type": "literal",
          "value": "Squamous Cell Carcinoma"
        }
      }
    ]
  }
}
"""

input = json.loads(big_json)
out = []
for binds in input['results']['bindings']:
    out.append({'label': binds['disease_type']['value'], 'value': binds['dt']['value']})

print(json.dumps(out, indent=2))
