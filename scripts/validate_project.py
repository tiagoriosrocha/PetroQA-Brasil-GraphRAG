import json
from pathlib import Path

base = Path(__file__).resolve().parents[1]
dataset_path = base / "data" / "petroqa_brasil_graphrag_150.json"
rdf_dir = base / "rdf" / "graphs"

with dataset_path.open("r", encoding="utf-8") as f:
    data = json.load(f)

ids = [item["id"] for item in data]
print("Items:", len(data))
print("Unique IDs:", len(set(ids)))
print("Missing questions:", sum(1 for item in data if not item.get("question")))
print("Missing contexts:", sum(1 for item in data if not item.get("context")))
print("Missing expected answers:", sum(1 for item in data if not item.get("expected_answer")))
print("Missing entities:", sum(1 for item in data if not item.get("entities")))
print("Missing reasoning paths:", sum(1 for item in data if not item.get("reasoning_path")))
print("RDF input graph files:", len(list(rdf_dir.glob("*.ttl"))))

forbidden = ["expected_answer", "hasExpectedAnswer", "hasAnswerText", "pq:Answer", "ans:", "original_question", "hasOriginalQuestion"]
leaky = []
for p in rdf_dir.glob("*.ttl"):
    txt = p.read_text(encoding="utf-8")
    if any(term in txt for term in forbidden):
        leaky.append(p.name)

print("RDF files with forbidden answer leakage:", len(leaky))
if leaky:
    print(leaky[:10])
