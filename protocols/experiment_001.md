# Experiment 001 — When One Sentence Is Enough

## Hypothesis
Longitudinal interaction history may alter the direction of completion elicited by the same ambiguous stimulus.

## Probe
Use a short ambiguous sentence. Keep the exact probe frozen within a comparison set.

## Conditions
- `long_existing`: existing long-running context
- `fresh`: new session, no prior project context
- `short_reconstructed`: minimal factual context reconstructed without narrative history
- optional cross-model equivalents

## Freeze
Record model identifier, quantization/build, runtime, context policy, temperature, reasoning configuration, seed if available, timestamp, and transport path.

## Procedure
1. Do not tell the model which behavior is being tested.
2. Present the frozen probe without steering.
3. Preserve the raw response verbatim.
4. Repeat each condition enough times to observe sampling variance.
5. Annotate only after generation.
6. Keep failures/timeouts as run records rather than deleting them.

## Primary labels
- relationship_completion
- character_completion
- user_preference_inference
- temporal_expansion
- future_projection
- omission_stop_recommendation
- unsupported_factual_invention

## Analysis
Compare label frequency, response length, evidence-to-inference hop count, grounding retention, and cross-run consistency.

## Threats to validity
Prompt leakage; context contamination; truncation policy; decoding variance; runtime/session failure; hidden provider changes; annotator ambiguity.

## Interpretation rule
A behavioral difference is evidence of a behavioral difference under the recorded conditions. It is not by itself evidence of a particular hidden mechanism.
