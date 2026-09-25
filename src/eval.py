import argparse, json
from collections import defaultdict
from pathlib import Path

LABELS = [
    "relationship_completion","character_completion","user_preference_inference",
    "temporal_expansion","future_projection","omission_stop_recommendation",
    "unsupported_factual_invention"
]

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
    out={"n_runs":len(rows),"groups":[]}
    for (model,condition), rs in sorted(groups.items()):
        ok=[r for r in rs if r.get("status")=="ok"]
        item={"model":model,"condition":condition,"n":len(rs),"n_ok":len(ok),"label_rates":{}}
        for label in LABELS:
            vals=[int(r.get("labels",{}).get(label,0)) for r in ok]
            item["label_rates"][label]=(sum(vals)/len(vals)) if vals else None
        lengths=[len(r.get("response","").split()) for r in ok]
        item["mean_response_words"]=(sum(lengths)/len(lengths)) if lengths else None
        out["groups"].append(item)
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
