# Persistent Attractors in Long-Context Human–LLM Interaction

An exploratory, reproducible evaluation project for studying whether different longitudinal interaction histories produce stable differences in model completion behavior under the same ambiguous stimulus.

## Research questions

1. Do long-running interaction histories produce reproducible behavioral attractors?
2. Can those attractors be separated from model, session, decoding, and prompt effects?
3. Can a model infer an aesthetic preference for omission — including when *not* to continue?

The project treats model outputs as behavioral observations. It does **not** infer consciousness, hidden state, or undocumented backend mechanisms from text alone.

## Experiment 001 — When One Sentence Is Enough

The first experiment tests a short ambiguous stimulus under controlled conditions:

- long existing context
- fresh context
- short reconstructed context
- repeated runs with frozen decoding settings
- cross-model comparison where possible

Primary annotation labels include relationship completion, character completion, user-preference inference, temporal expansion, future projection, omission/stop recommendation, and unsupported factual invention.

## Repository structure

- `protocols/` frozen experimental procedures
- `prompts/` prompt fixtures and condition metadata
- `runs/` raw run records (anonymize before committing)
- `annotations/` annotation schema and labels
- `src/` small Python evaluation harness
- `results/` generated summaries
- `tests/` basic parser/metric tests

## Grounding rules

- Observation is not mechanism.
- Unsupported backend explanations are `UNKNOWN`.
- Generated success may validate a hypothesis; it does not become Ground Truth by default.
- Do not reveal the target behavioral label to the evaluated model before the probe.
- Preserve negative and non-replicating results.

## Quick start

```bash
python src/eval.py --runs runs/example_runs.jsonl --out results/summary.json
```

This v0.1 intentionally begins with a provider-neutral offline evaluator. Raw model outputs can be collected manually or through a later adapter without changing the annotation or analysis format.

## Synthetic baseline check

`runs/synthetic_exp001_baseline.jsonl` contains fabricated, pre-labeled records for checking the evaluation pipeline; it is not experimental evidence. Its valid-run AER is 0.25 for `fresh`, 0.5 for `short_reconstructed`, and 0.75 for `long_existing`, so the expected long-minus-fresh `delta_aer` is 0.5. A timeout remains recorded but is excluded from the denominator. A fresh response labeled only as `unsupported_factual_invention` does not count as attractor emergence.

```bash
python src/eval.py --runs runs/synthetic_exp001_baseline.jsonl --out results/synthetic_summary.json
```
