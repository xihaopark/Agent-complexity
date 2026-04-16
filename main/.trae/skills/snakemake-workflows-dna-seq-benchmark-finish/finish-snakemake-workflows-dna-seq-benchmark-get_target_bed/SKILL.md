---
name: finish-snakemake-workflows-dna-seq-benchmark-get_target_bed
description: Use this skill when orchestrating the retained "get_target_bed" step of the snakemake workflows dna seq benchmark finish finish workflow. It keeps the get target bed stage tied to upstream `get_liftover_track` and the downstream handoff to `postprocess_target_bed`. It tracks completion via `results/finish/get_target_bed.done`.
metadata:
  workflow_id: dna-seq-benchmark-finish
  workflow_name: snakemake workflows dna seq benchmark finish
  step_id: get_target_bed
  step_name: get target bed
---

# Scope
Use this skill only for the `get_target_bed` step in `dna-seq-benchmark-finish`.

## Orchestration
- Upstream requirements: `get_liftover_track`
- Step file: `finish/dna-seq-benchmark-finish/steps/get_target_bed.smk`
- Config file: `finish/dna-seq-benchmark-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/get_target_bed.done`
- Representative outputs: `results/finish/get_target_bed.done`
- Execution targets: `get_target_bed`
- Downstream handoff: `postprocess_target_bed`

## Guardrails
- Treat `results/finish/get_target_bed.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/get_target_bed.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `postprocess_target_bed` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/get_target_bed.done` exists and `postprocess_target_bed` can proceed without re-running get target bed.
