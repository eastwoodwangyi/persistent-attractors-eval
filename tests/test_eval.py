import sys
sys.path.insert(0, "src")
from eval import summarize

def test_summary():
    rows=[{"model":"A","condition":"fresh","status":"ok","response":"one two",
           "labels":{"omission_stop_recommendation":1}}]
    s=summarize(rows)
    assert s["n_runs"]==1
    assert s["groups"][0]["label_rates"]["omission_stop_recommendation"]==1.0
