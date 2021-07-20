Semantic Services Middleware
============================

Purpose
-------

The semantic services middleware stores any semantically created information about entities in PRISM.
This information will be represented in RDF and stored in a triplestore.
Other services will be able to access the information from both a REST API or through direct SPARQL queries.

Examples of Entities
--------------------

* Collection
 - Name of collection
 - Publications related to collection
 - Features present in collection
* Subject
 - Curated clinical data
* File
* Feature?

Uses
----

Thanks to the graph nature of datastore, the semantic services layer is the ideal place to perform discovery queries.
Any user facing tool could ask for all files in a collection, or all subjects with some feature, without having to iterate through all of the data managers.

Requirements
------------

* Starting List of Entities
 - Collection
 - Subject (a human in a collection, potentially multiple collections)
 - File (a data artifact present in one of the data managers, part of a collection)
* unique resource identifier (URI) format for each of these entities

Architecture
------------

* Triplestore
 - ~GraphDB free edition~ (find an open source triplestore that meets *our needs*)
* REST API
 - FastAPI python

A small version of this is currently running on the kubernetes system for the demo, this would need to be expanded for the full project.

API Interface
-------------

The API interface documentation will be automatically generated from the code using Swagger.
The basic pattern will be endpoints that list available filters and then endpoints that return entities that correspond to said features.

```
GET /info/subjects
[ 
 'age': {'type': 'float', 'min': 0, 'max': 90},
 'cancer_stage': {'type': 'uris', 'options': [('<uri:stage1>', 'Stage 1'), ('<uri:stage1A>', 'Stage 1A')]},
 ...
]
```

Workflow
--------

When new entities are added to PRISM, something will need to create the RDF and load it into the triplestore for the semantic services layer to stay up to date.
For any entities added by Posda this could just be an additional script added to the publishing step of Posda.
However, if we are planning on adding entities directly, some step will need to be added to that process to generate the RDF.