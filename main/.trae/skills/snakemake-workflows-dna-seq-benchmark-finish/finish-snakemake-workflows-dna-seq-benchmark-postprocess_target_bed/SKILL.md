---
name: finish-snakemake-workflows-dna-seq-benchmark-postprocess_target_bed
description: Use this skill when orchestrating the retained "postprocess_target_bed" step of the snakemake workflows dna seq benchmark finish finish workflow. It keeps the postprocess target bed stage tied to upstream `get_target_bed` and the downstream handoff to `get_reference`. It tracks completion via `results/finish/postprocess_target_bed.done`.
metadata:
  workflow_id: dna-seq-benchmark-finish
  workflow_name: snakemake workflows dna seq benchmark finish
  step_id: postprocess_target_bed
  step_name: postprocess target bed
---

# Scope
Use this skill only for the `postprocess_target_bed` step in `dna-seq-benchmark-finish`.

## Orchestration
- Upstream requirements: `get_target_bed`
- Step file: `finish/dna-seq-benchmark-finish/steps/postprocess_target_bed.smk`
- Config file: `finish/dna-seq-benchmark-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/postprocess_target_bed.done`
- Representative outputs: `results/finish/postprocess_target_bed.done`
- Execution targets: `postprocess_target_bed`
- Downstream handoff: `get_reference`

## Guardrails
- Treat `results/finish/postprocess_target_bed.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/postprocess_target_bed.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `get_reference` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/postprocess_target_bed.done` exists and `get_reference` can proceed without re-running postprocess target bed.
