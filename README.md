# PetroQA-Brasil

**PetroQA-Brasil** is a Portuguese Question Answering (QA) dataset for **petroleum geoscience**, designed to evaluate evidence-grounded and relation-aware reasoning in Retrieval-Augmented Generation (RAG), GraphRAG, and ontology-enriched retrieval pipelines.

The dataset focuses on questions that require more than direct span extraction. Each item is designed to connect geological entities, properties, processes, and roles, such as sedimentary basins, stratigraphic units, lithologies, reservoirs, source rocks, seals, faults, depositional environments, and petrophysical properties.

Repository: <https://github.com/tiagoriosrocha/PetroQA-Brasil>

---

## 1. Motivation

Most QA datasets used in NLP are general-domain and English-centered. Petroleum-geoscience documents, however, contain specialized terminology and dense relational knowledge. A correct answer often depends on connecting entities and concepts such as:

```text
evaporite -> low permeability -> geological seal -> hydrocarbon retention
```

or:

```text
formation -> carbonate lithology -> porosity/permeability -> reservoir function
```

This makes petroleum geoscience a challenging domain for evaluating:

- traditional RAG;
- dense retrieval;
- GraphRAG;
- ontology-enriched retrieval;
- evidence-grounded large language models;
- relation-aware question answering.

**PetroQA-Brasil** was created to support controlled experiments in this setting.

---

## 2. Dataset Overview

The current version contains:

| Property | Value |
|---|---:|
| Questions | 150 |
| Language | Portuguese |
| Domain | Petroleum geoscience |
| Unique source URLs | 20 |
| Mean source blocks per item | 1.98 |
| Mean question length | 12.9 words |
| Mean context length | 73.8 words |
| Context length range | 21--180 words |
| Mean expected-answer length | 17.3 words |

The dataset is available in two main forms:

1. **Original QA dataset**  
   Contains question, context, expected answer, inference type, and source information.

2. **GraphRAG-oriented dataset**  
   Extends the original dataset with entities, relations, reasoning paths, number of hops, difficulty labels, ontology requirement flags, retrieval scope, and supporting facts.

---

## 3. Dataset Files

Recommended repository structure:

```text
PetroQA-Brasil/
├── data/
│   ├── petroqa_brasil_150.json
│   ├── petroqa_brasil_150.csv
│   ├── petroqa_brasil_graphrag_150.json
│   ├── petroqa_brasil_graphrag_150.csv
│   ├── sources.csv
│   └── audit/
│       ├── audit_questions_vs_sources_petroqa_brasil_graphrag.csv
│       ├── audit_questions_vs_sources_petroqa_brasil_graphrag_por_questao.csv
│       └── audit_questions_vs_sources_summary.json
├── scripts/
│   ├── validate_dataset.py
│   ├── json_to_csv.py
│   ├── build_audit_table.py
│   └── export_contexts.py
├── docs/
│   └── paper/
│       ├── petroqa_brasil_acl_dataset_format.tex
│       └── petroqa_brasil_acl_dataset_format.pdf
├── README.md
└── LICENSE
```

Depending on the release, file names may vary slightly. The important distinction is between the **standard QA version**, the **GraphRAG-oriented version**, and the **audit files**.

---

## 4. Standard Dataset Schema

Each item in the standard dataset follows this structure:

```json
{
  "id": 1,
  "question": "Que entidade geológica explica a retenção do petróleo abaixo dos reservatórios carbonáticos da Bacia de Santos?",
  "context": [
    [
      "Source title",
      [
        "Literal paragraph from the source.",
        "Another literal paragraph from the source."
      ]
    ]
  ],
  "expected_answer": "A camada de sal/evaporitos é a entidade que atua como barreira ou selo, mantendo os hidrocarbonetos retidos nos reservatórios carbonáticos do pré-sal.",
  "tipo_inferencia": "selo_e_retencao",
  "source": [
    "https://example.org/source"
  ]
}
```

### Fields

| Field | Description |
|---|---|
| `id` | Unique question identifier. |
| `question` | Natural-language question in Portuguese. |
| `context` | Literal context excerpts from public Portuguese geoscience sources. |
| `expected_answer` | Reference answer grounded in the context. |
| `tipo_inferencia` | Inference type used for diagnostic analysis. |
| `source` | Source URL(s) used to construct the context. |

The `tipo_inferencia` field should **not** be provided to QA models as part of the input. It is intended for evaluation and error analysis.

---

## 5. GraphRAG-Oriented Dataset Schema

The GraphRAG-oriented version extends the standard schema:

```json
{
  "id": 1,
  "question": "Como as evidências conectam camada de sal à retenção ou migração de hidrocarbonetos?",
  "original_question": "Que entidade geológica explica a retenção do petróleo abaixo dos reservatórios carbonáticos da Bacia de Santos?",
  "context": [...],
  "expected_answer": "...",
  "tipo_inferencia": "selo_e_retencao",
  "source": [...],
  "entities": [
    "Bacia de Santos",
    "reservatórios carbonáticos",
    "camada de sal",
    "selo",
    "hidrocarbonetos"
  ],
  "relations": [
    {
      "head": "camada de sal",
      "relation": "acts_as",
      "tail": "selo geológico"
    }
  ],
  "reasoning_path": [
    "camada de sal",
    "baixa permeabilidade",
    "selo geológico",
    "retenção de hidrocarbonetos"
  ],
  "num_hops": 4,
  "answer_type": "entity_role",
  "difficulty": "hard",
  "requires_ontology": true,
  "retrieval_scope": "multi_document",
  "supporting_facts": [
    {
      "source_title": "Source title",
      "text": "Literal evidence excerpt.",
      "role": "evidence"
    }
  ]
}
```

### Additional GraphRAG Fields

| Field | Description |
|---|---|
| `original_question` | Question from the original dataset. |
| `entities` | Geological/domain entities associated with the item. |
| `relations` | Relation triples derived from the reasoning path. |
| `reasoning_path` | Expected conceptual path required to answer. |
| `num_hops` | Estimated number of reasoning hops. |
| `answer_type` | Type of answer expected, such as `entity_role` or `temporal_relation`. |
| `difficulty` | Estimated difficulty: `easy`, `medium`, or `hard`. |
| `requires_ontology` | Whether ontology-like normalization is expected to help. |
| `retrieval_scope` | Expected retrieval scope: `single_passage`, `multi_passage`, or `multi_document`. |
| `supporting_facts` | Literal evidence excerpts used to support the answer. |

This version is intended to make the benchmark more diagnostic for GraphRAG and ontology-enriched retrieval.

---

## 6. Inference Types

The dataset contains several types of geological inference:

| Inference Type | Description |
|---|---|
| `composicional_petrofisica` | Connects lithological composition to petrophysical properties or reservoir function. |
| `interpretativa` | Requires geological interpretation from evidence. |
| `temporal_estratigrafica` | Requires temporal or stratigraphic reasoning. |
| `espacial` | Requires spatial reasoning between basins, fields, units, or structures. |
| `entidade_estratigrafica` | Identifies or relates stratigraphic entities. |
| `selo_e_retencao` | Connects seals, barriers, evaporites, and hydrocarbon retention. |
| `ontologica_entidade_funcao` | Maps geological entities to functional roles. |
| `ambiente_deposicional` | Infers depositional environment from evidence. |
| `processual_migracao` | Involves hydrocarbon migration processes. |
| `processual_deposicional` | Involves depositional processes or events. |
| `estrutural` | Requires structural interpretation. |
| `geracao_de_hidrocarbonetos` | Relates source rocks, organic matter, and hydrocarbon generation. |

---

## 7. Audit Files

The audit files connect each question to its evidence and source URLs.

### Audit by context paragraph

File:

```text
audit_questions_vs_sources_petroqa_brasil_graphrag.csv
```

This file contains one row per context paragraph. It is useful for manually checking whether each evidence fragment supports the expected answer.

Main columns:

| Column | Description |
|---|---|
| `id` | Question ID. |
| `question` | GraphRAG-oriented question. |
| `original_question` | Original question. |
| `expected_answer` | Reference answer. |
| `tipo_inferencia` | Inference type. |
| `source_block_index` | Context block index. |
| `paragraph_index` | Paragraph index inside the block. |
| `source_title` | Title of the source block. |
| `source_url` | Source URL. |
| `context_text` | Literal evidence excerpt. |
| `entities` | Extracted entities. |
| `relations` | Relation triples. |
| `reasoning_path` | Expected reasoning path. |

### Audit by question

File:

```text
audit_questions_vs_sources_petroqa_brasil_graphrag_por_questao.csv
```

This file contains one row per question, with the context concatenated. It is useful for spreadsheet-based review or direct QA evaluation.

---

## 8. Evaluation Settings

PetroQA-Brasil supports two main evaluation settings.

### 8.1 Given-Context QA

The model receives:

```text
question + gold context
```

The goal is to evaluate answer generation and reasoning independently from retrieval.

Recommended metrics:

- Exact Match;
- Token F1;
- Answer Relevancy;
- Correctness;
- Completeness;
- Faithfulness;
- Geological Adequacy.

### 8.2 Retrieval-Based QA

The model receives only the question and must retrieve evidence before answering.

Recommended methods:

- BM25 + LLM;
- Dense RAG + LLM;
- GraphRAG;
- GraphRAG + ontology;
- LLM-only baseline;
- Human baseline.

Recommended retrieval metrics:

- Context Precision;
- Context Recall;
- Evidence Coverage;
- Supporting-fact Recall.

---

## 9. GraphRAG Evaluation

The GraphRAG-oriented version is designed to test whether a system can recover or approximate the expected reasoning path.

Recommended additional metrics:

| Metric | Description |
|---|---|
| Entity Recall | Whether retrieved context/subgraph contains expected entities. |
| Relation Recall | Whether retrieved context/subgraph contains expected relations. |
| Path Coverage | Whether the retrieved subgraph covers the expected `reasoning_path`. |
| Ontology Alignment | Whether the answer maps entities to correct geological roles. |
| Relation-Aware Faithfulness | Whether the answer is faithful not only to text but also to the expected relations. |

Example expected reasoning path:

```text
camada de sal -> baixa permeabilidade -> selo geológico -> retenção de hidrocarbonetos
```

A GraphRAG system should ideally retrieve a subgraph containing these entities and relations.

---

## 10. Suggested Baselines

A complete benchmark should report at least:

| Method | Description |
|---|---|
| LLM-only | Model receives only the question. |
| BM25 + LLM | Sparse retrieval followed by generation. |
| Dense RAG + LLM | Embedding-based retrieval followed by generation. |
| GraphRAG | Graph-based retrieval followed by generation. |
| GraphRAG + Ontology | Graph retrieval enriched with ontology matching. |
| Human | Domain-aware human answer using only the context. |

Suggested result table:

| Method | EM | F1 | Faithfulness | Correctness | Geological Adequacy |
|---|---:|---:|---:|---:|---:|
| LLM-only | -- | -- | -- | -- | -- |
| BM25 + LLM | -- | -- | -- | -- | -- |
| Dense RAG + LLM | -- | -- | -- | -- | -- |
| GraphRAG | -- | -- | -- | -- | -- |
| GraphRAG + Ontology | -- | -- | -- | -- | -- |
| Human | -- | -- | -- | -- | -- |

---

## 11. Example

Example item:

```json
{
  "id": 1,
  "question": "Como as evidências conectam camada de sal à retenção ou migração de hidrocarbonetos?",
  "original_question": "Que entidade geológica explica a retenção do petróleo abaixo dos reservatórios carbonáticos da Bacia de Santos?",
  "expected_answer": "A camada de sal/evaporitos é a entidade que atua como barreira ou selo, mantendo os hidrocarbonetos retidos nos reservatórios carbonáticos do pré-sal.",
  "tipo_inferencia": "selo_e_retencao",
  "reasoning_path": [
    "camada de sal",
    "baixa permeabilidade",
    "selo geológico",
    "retenção de hidrocarbonetos"
  ],
  "requires_ontology": true,
  "retrieval_scope": "multi_document"
}
```

---

## 12. How to Use

### Load the JSON dataset

```python
import json

with open("data/petroqa_brasil_graphrag_150.json", "r", encoding="utf-8") as f:
    dataset = json.load(f)

print(len(dataset))
print(dataset[0]["question"])
```

### Load the CSV dataset

```python
import pandas as pd

df = pd.read_csv("data/petroqa_brasil_graphrag_150.csv")
print(df.head())
```

### Example input for QA evaluation

```python
item = dataset[0]

question = item["question"]
context = " ".join(
    paragraph
    for block in item["context"]
    for paragraph in block[1]
)

expected_answer = item["expected_answer"]
```

---

## 13. Recommended Validation Checks

Before running experiments, verify:

- all IDs are unique;
- every item has a non-empty question;
- every item has a non-empty context;
- every item has a non-empty expected answer;
- every item has at least one source URL;
- GraphRAG items have `entities`, `relations`, and `reasoning_path`;
- `tipo_inferencia` is not included in the model prompt;
- source excerpts are sufficient to support the expected answer.

---

## 14. Limitations

The current version has important limitations:

- it contains 150 curated items, which is appropriate for evaluation and error analysis but not for training large models from scratch;
- it focuses on Portuguese petroleum geoscience and does not cover all geoscience subdomains;
- the GraphRAG-oriented fields were derived from the curated dataset and should be manually audited before publication as a final benchmark release;
- inter-annotator agreement has not yet been computed;
- human performance has not yet been measured;
- full source documents are not distributed, only selected excerpts and source URLs.

---

## 15. Ethics Statement

The dataset was constructed from public Portuguese-language sources and preserves only short excerpts required for QA evaluation. It is intended for research on information retrieval, question answering, and ontology-guided reasoning in petroleum geoscience.

Users should verify the licensing and usage conditions of the original sources before redistributing large portions of source text or reconstructing full documents.

The dataset does not intentionally include personal data or sensitive personal information. Because it focuses on technical geoscience content, risks related to personally identifiable information are expected to be low.

The dataset should not be used as a substitute for professional geological interpretation in operational, safety-critical, legal, or investment contexts.

---

## 16. Citation

If you use this dataset, please cite:

```bibtex
@misc{rocha2026petroqa,
  title        = {PetroQA-Brasil: A Portuguese Question Answering Dataset for Relational Inference in Petroleum Geoscience},
  author       = {da Rocha, T. R. and Netto, J. and Becker, K.},
  year         = {2026},
  howpublished = {\url{https://github.com/tiagoriosrocha/PetroQA-Brasil}},
  note         = {Dataset and benchmark for Portuguese petroleum-geoscience QA}
}
```

---

## 17. License

A license should be added before public release.

Recommended options:

- **CC BY 4.0** for dataset metadata and annotations;
- verify original source licenses before redistributing extracted text;
- if source licensing is uncertain, distribute only metadata, questions, answers, source URLs, and short excerpts under fair-use/research assumptions where applicable.

---

## 18. Contact

For questions or contributions, please contact:

- **T. R. da Rocha**  
  Instituto Federal do Rio Grande do Sul  
  Universidade Federal do Rio Grande do Sul  
  <tiago.rios@ibiruba.ifrs.edu.br>

- **J. Netto**  
  Universidade Federal do Rio Grande do Sul  
  <netto@inf.ufrgs.br>

- **K. Becker**  
  Universidade Federal do Rio Grande do Sul  
  <karin.becker@inf.ufrgs.br>
