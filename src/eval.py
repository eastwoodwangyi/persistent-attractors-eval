import argparse, json
from collections import defaultdict
from pathlib import Path

LABELS = [
    "relationship_completion","character_completion","user_preference_inference",
    "temporal_expansion","future_projection","omission_stop_recommendation",
    "unsupported_factual_invention"
]
ATTRACTOR_LABELS = LABELS[:-1]  # Grounding failure alone is not attractor emergence.

def has_attractor_emergence(row):
    """A valid response emerges if any candidate behavioral label is present."""
    labels = row.get("labels", {})
    return any(int(labels.get(label, 0)) == 1 for label in ATTRACTOR_LABELS)

def load_jsonl(path):
    rows=[]
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows

def summarize(rows):
    groups=defaultdict(list)
    for r in rows:
        groups[(r.get("model","UNKNOWN"), r.get("condition","UNKNOWN"))].append(r)
    out={"n_runs":len(rows),"groups":[],"comparisons":[]}
    for (model,condition), rs in sorted(groups.items()):
        ok=[r for r in rs if r.get("status")=="ok"]
        item={"model":model,"condition":condition,"n":len(rs),"n_ok":len(ok),"label_rates":{}}
        item["attractor_emergence_rate"]=(
            sum(has_attractor_emergence(r) for r in ok)/len(ok) if ok else None
        )
        for label in LABELS:
            vals=[int(r.get("labels",{}).get(label,0)) for r in ok]
            item["label_rates"][label]=(sum(vals)/len(vals)) if vals else None
        lengths=[len(r.get("response","").split()) for r in ok]
        item["mean_response_words"]=(sum(lengths)/len(lengths)) if lengths else None
        out["groups"].append(item)
    by_model=defaultdict(dict)
    for item in out["groups"]:
        by_model[item["model"]][item["condition"]]=item["attractor_emergence_rate"]
    for model, conditions in sorted(by_model.items()):
        fresh=conditions.get("fresh")
        long_existing=conditions.get("long_existing")
        if fresh is not None and long_existing is not None:
            out["comparisons"].append({
                "model":model,"condition_a":"long_existing","condition_b":"fresh",
                "delta_aer":long_existing-fresh,
            })
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--runs", required=True)
    ap.add_argument("--out", required=True)
    args=ap.parse_args()
    result=summarize(load_jsonl(args.runs))
    Path(args.out).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
