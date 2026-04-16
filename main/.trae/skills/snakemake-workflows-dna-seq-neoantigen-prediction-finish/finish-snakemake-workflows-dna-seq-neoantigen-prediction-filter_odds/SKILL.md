---
name: finish-snakemake-workflows-dna-seq-neoantigen-prediction-filter_odds
description: Use this skill when orchestrating the retained "filter_odds" step of the snakemake workflows dna seq neoantigen prediction finish finish workflow. It keeps the filter odds stage tied to upstream `filter_by_annotation` and the downstream handoff to `gather_calls`. It tracks completion via `results/finish/filter_odds.done`.
metadata:
  workflow_id: dna-seq-neoantigen-prediction-finish
  workflow_name: snakemake workflows dna seq neoantigen prediction finish
  step_id: filter_odds
  step_name: filter odds
---

# Scope
Use this skill only for the `filter_odds` step in `dna-seq-neoantigen-prediction-finish`.

## Orchestration
- Upstream requirements: `filter_by_annotation`
- Step file: `finish/dna-seq-neoantigen-prediction-finish/steps/filter_odds.smk`
- Config file: `finish/dna-seq-neoantigen-prediction-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/filter_odds.done`
- Representative outputs: `results/finish/filter_odds.done`
- Execution targets: `filter_odds`
- Downstream handoff: `gather_calls`

## Guardrails
- Treat `results/finish/filter_odds.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/filter_odds.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `gather_calls` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/filter_odds.done` exists and `gather_calls` can proceed without re-running filter odds.
