---
name: finish-snakemake-workflows-dna-seq-benchmark-get_confidence_bed
description: Use this skill when orchestrating the retained "get_confidence_bed" step of the snakemake workflows dna seq benchmark finish finish workflow. It keeps the get confidence bed stage tied to upstream `normalize_truth` and the downstream handoff to `get_liftover_track`. It tracks completion via `results/finish/get_confidence_bed.done`.
metadata:
  workflow_id: dna-seq-benchmark-finish
  workflow_name: snakemake workflows dna seq benchmark finish
  step_id: get_confidence_bed
  step_name: get confidence bed
---

# Scope
Use this skill only for the `get_confidence_bed` step in `dna-seq-benchmark-finish`.

## Orchestration
- Upstream requirements: `normalize_truth`
- Step file: `finish/dna-seq-benchmark-finish/steps/get_confidence_bed.smk`
- Config file: `finish/dna-seq-benchmark-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/get_confidence_bed.done`
- Representative outputs: `results/finish/get_confidence_bed.done`
- Execution targets: `get_confidence_bed`
- Downstream handoff: `get_liftover_track`

## Guardrails
- Treat `results/finish/get_confidence_bed.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/get_confidence_bed.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `get_liftover_track` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/get_confidence_bed.done` exists and `get_liftover_track` can proceed without re-running get confidence bed.
