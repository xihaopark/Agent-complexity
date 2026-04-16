---
name: finish-snakemake-workflows-dna-seq-benchmark-get_liftover_track
description: Use this skill when orchestrating the retained "get_liftover_track" step of the snakemake workflows dna seq benchmark finish finish workflow. It keeps the get liftover track stage tied to upstream `get_confidence_bed` and the downstream handoff to `get_target_bed`. It tracks completion via `results/finish/get_liftover_track.done`.
metadata:
  workflow_id: dna-seq-benchmark-finish
  workflow_name: snakemake workflows dna seq benchmark finish
  step_id: get_liftover_track
  step_name: get liftover track
---

# Scope
Use this skill only for the `get_liftover_track` step in `dna-seq-benchmark-finish`.

## Orchestration
- Upstream requirements: `get_confidence_bed`
- Step file: `finish/dna-seq-benchmark-finish/steps/get_liftover_track.smk`
- Config file: `finish/dna-seq-benchmark-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/get_liftover_track.done`
- Representative outputs: `results/finish/get_liftover_track.done`
- Execution targets: `get_liftover_track`
- Downstream handoff: `get_target_bed`

## Guardrails
- Treat `results/finish/get_liftover_track.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/get_liftover_track.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `get_target_bed` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/get_liftover_track.done` exists and `get_target_bed` can proceed without re-running get liftover track.
