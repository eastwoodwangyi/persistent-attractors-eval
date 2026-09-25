"""Validate manually collected Experiment 001 observations before evaluation."""

import argparse
import json
from collections import Counter
from datetime import datetime

from eval import LABELS, load_jsonl

CONDITIONS = {"fresh", "short_reconstructed", "long_existing"}
REQUIRED = {"run_id", "condition", "model", "status", "response", "labels",
            "timestamp", "probe", "context_policy", "decoding"}


def validate(rows):
    errors = []
    ids = set()
    for number, row in enumerate(rows, 1):
        missing = REQUIRED - row.keys()
        if missing:
            errors.append(f"row {number}: missing {', '.join(sorted(missing))}")
            continue
        if row["run_id"] in ids:
            errors.append(f"row {number}: duplicate run_id")
        if not isinstance(row["run_id"], str) or not row["run_id"].strip():
            errors.append(f"row {number}: missing run_id")
        ids.add(row["run_id"])
        if row["condition"] not in CONDITIONS:
            errors.append(f"row {number}: unknown condition")
        if not isinstance(row["model"], str) or not row["model"].strip():
            errors.append(f"row {number}: missing model identifier")
        if row["status"] not in {"ok", "timeout", "error"}:
            errors.append(f"row {number}: invalid status")
        try:
            datetime.fromisoformat(row["timestamp"].replace("Z", "+00:00"))
        except (ValueError, AttributeError):
            errors.append(f"row {number}: invalid timestamp")
        if not isinstance(row["probe"], str) or not row["probe"].strip():
            errors.append(f"row {number}: missing probe")
        if not isinstance(row["context_policy"], str) or not row["context_policy"].strip():
            errors.append(f"row {number}: missing context policy")
        if not isinstance(row["decoding"], dict) or not row["decoding"]:
            errors.append(f"row {number}: missing decoding settings")
        if row["status"] == "ok":
            if not isinstance(row["response"], str) or not row["response"].strip():
                errors.append(f"row {number}: empty successful response")
            if not isinstance(row["labels"], dict) or set(row["labels"]) != set(LABELS):
                errors.append(f"row {number}: incomplete labels")
            elif any(type(value) is not int or value not in (0, 1)
                     for value in row["labels"].values()):
                errors.append(f"row {number}: labels must be 0 or 1")
    for model in {row.get("model") for row in rows if row.get("model")}:
        probes = {row.get("probe") for row in rows if row.get("model") == model}
        if len(probes) != 1:
            errors.append(f"model {model}: probe differs across runs")
        settings = {json.dumps(row.get("decoding"), sort_keys=True)
                    for row in rows if row.get("model") == model}
        if len(settings) != 1:
            errors.append(f"model {model}: decoding differs across runs")
    return errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--runs", required=True)
    args = parser.parse_args()
    rows = load_jsonl(args.runs)
    errors = validate(rows)
    for error in errors:
        print(error)
    counts = Counter(row.get("condition") for row in rows)
    print(f"Validated {len(rows)} records; condition counts: {dict(counts)}")
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
