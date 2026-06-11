# PetroQA-Brasil input RDF graphs with GeoCore classes

This package contains one RDF/Turtle input graph per question.

These files are intended to be sent to a QA model together with the question.
They do not include gold answers or answer-specific RDF vocabulary.

## What was removed to avoid leakage

The generated graphs do not include:

- `expected_answer`
- `pq:hasExpectedAnswer`
- `pq:hasAnswerText`
- `pq:Answer`
- `ans:*`
- `original_question`
- `pq:hasOriginalQuestion`

## What remains in the graph

Each input graph includes:

- the question text;
- inference metadata;
- evidence excerpts from the original source texts;
- source URLs;
- geological entities;
- relation assertions;
- reasoning path steps;
- GeoCore class typing.

## GeoCore classes used

Entities are typed using a GeoCore-compatible namespace:

```turtle
@prefix geocore: <https://www.inf.ufrgs.br/bdi/ontologies/geocore.owl#> .
```

Main classes used:

- `geocore:GeologicalObject`
- `geocore:GeologicalProcess`
- `geocore:GeologicalAge`
- `geocore:GeologicalStructure`
- `geocore:GeologicalTimeInterval`
- `geocore:EarthMaterial`
- `geocore:AmountOfMineral`
- `geocore:AmountOfRock`
- `geocore:EarthFluid`
- `geocore:UnconsolidatedEarthMaterial`
- `geocore:GeologicalBoundary`
- `geocore:GeologicalContact`

## Files

- `graphs/question_001_input.ttl` ... `graphs/question_150_input.ttl`
- `petroqa_brasil_all_input_graphs_geocore.ttl`
- `petroqa_input_graph_schema.ttl`
- `geocore_compatibility_layer.ttl`
- `input_rdf_graph_index.csv`
- `input_rdf_graphs_validation.json`

## Validation

Generated RDF input files: 150
Files with forbidden answer-vocabulary leakage: 0
Files containing the exact expected answer string: 0
