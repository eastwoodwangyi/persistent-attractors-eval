import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from validate_real_runs import CANONICAL_PROBE, validate


def sample(condition="fresh"):
    return {"run_id":"one","condition":condition,"model":"MODEL_BUILD",
            "status":"ok","response":"raw response","timestamp":"2026-09-25T09:00:00Z",
            "probe":CANONICAL_PROBE,"context_policy":"new session 1",
            "decoding":{"temperature":0,"seed":None},
            "labels":{label:0 for label in (
                "relationship_completion","character_completion","user_preference_inference",
                "temporal_expansion","future_projection","omission_stop_recommendation",
                "unsupported_factual_invention")}}


def test_valid_run_and_preserved_timeout():
    failed=sample("long_existing")
    failed.update(run_id="two",status="timeout",response="",labels={})
    assert validate([sample(), failed])==[]


def test_detects_noncomparable_and_incomplete_runs():
    other=sample("long_existing")
    other.update(run_id="two",probe="different probe",decoding={"temperature":1})
    other["labels"].pop("relationship_completion")
    errors=validate([sample(),other])
    assert any("probe differs" in error for error in errors)
    assert any("decoding differs" in error for error in errors)
    assert any("incomplete labels" in error for error in errors)

def test_rejects_fullwidth_question_mark():
    row=sample()
    row["probe"]="喜歡昨夜的溫柔嗎？"
    assert any("frozen fixture" in error for error in validate([row]))
