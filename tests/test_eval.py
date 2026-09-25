import sys
sys.path.insert(0, "src")
from eval import has_attractor_emergence, summarize

def run(condition, labels=None, status="ok", model="A"):
    return {"model":model,"condition":condition,"status":status,"labels":labels or {}}

def test_summary():
    rows=[{"model":"A","condition":"fresh","status":"ok","response":"one two",
           "labels":{"omission_stop_recommendation":1}}]
    s=summarize(rows)
    assert s["n_runs"]==1
    assert s["groups"][0]["label_rates"]["omission_stop_recommendation"]==1.0
    assert s["groups"][0]["attractor_emergence_rate"]==1.0

def test_candidate_labels_and_grounding_failure():
    assert not has_attractor_emergence(run("fresh", {"unsupported_factual_invention":1}))
    for label in ("relationship_completion", "character_completion",
                  "user_preference_inference", "temporal_expansion",
                  "future_projection", "omission_stop_recommendation"):
        assert has_attractor_emergence(run("fresh", {label:1}))

def test_rate_uses_valid_runs_only():
    rows=[run("fresh", {"relationship_completion":1}), run("fresh"),
          run("fresh", {"unsupported_factual_invention":1}),
          run("fresh", {"relationship_completion":1}, status="timeout")]
    group=summarize(rows)["groups"][0]
    assert group["n"]==4 and group["n_ok"]==3
    assert group["attractor_emergence_rate"]==1/3

def test_long_fresh_comparison_is_within_model():
    rows=[run("fresh", {"relationship_completion":1})]+[run("fresh") for _ in range(3)]
    rows += [run("long_existing", {"character_completion":1}) for _ in range(3)]
    rows += [run("long_existing")]
    rows += [run("fresh", {"relationship_completion":1}, model="B")]
    assert summarize(rows)["comparisons"]==[{
        "model":"A","condition_a":"long_existing","condition_b":"fresh",
        "delta_aer":0.5,
    }]

def test_missing_or_invalid_condition_has_no_comparison():
    assert summarize([run("fresh")])["comparisons"]==[]
    assert summarize([run("fresh"), run("long_existing", status="timeout")])["comparisons"]==[]
