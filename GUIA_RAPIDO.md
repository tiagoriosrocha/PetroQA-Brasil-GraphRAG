# Guia rápido — PetroQA-Brasil GraphRAG

Este pacote contém a versão GraphRAG do projeto PetroQA-Brasil.

## Pastas

- `data/`: dataset GraphRAG em JSON e CSV.
- `audit/`: arquivos CSV de auditoria conectando perguntas, contextos e fontes.
- `rdf/`: grafos RDF/Turtle sem vazamento de resposta, com classes compatíveis com GeoCore.
- `rdf/graphs/`: um grafo RDF por questão.
- `docs/`: templates de prompt para GraphQA e GraphRAG.
- `paper/`: arquivos do artigo, quando disponíveis.
- `scripts/`: scripts simples de validação.

## Arquivos principais

- `data/petroqa_brasil_graphrag_150.json`
- `data/petroqa_brasil_graphrag_150.csv`
- `audit/audit_questions_vs_sources_petroqa_brasil_graphrag.csv`
- `audit/audit_questions_vs_sources_petroqa_brasil_graphrag_por_questao.csv`
- `rdf/petroqa_brasil_all_input_graphs_geocore.ttl`
- `rdf/input_rdf_graph_index.csv`
- `rdf/graphs/question_001_input.ttl` até `question_150_input.ttl`

## Validação

Execute:

```bash
python scripts/validate_project.py
```

Os grafos RDF de entrada não incluem `expected_answer`, `hasExpectedAnswer`, `hasAnswerText`, `pq:Answer`, `ans:*`, `original_question` ou `hasOriginalQuestion`.
