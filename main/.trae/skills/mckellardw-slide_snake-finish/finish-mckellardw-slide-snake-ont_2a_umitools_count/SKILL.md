---
name: finish-mckellardw-slide-snake-ont_2a_umitools_count
description: Use this skill when orchestrating the retained "ont_2a_umitools_count" step of the mckellardw slide_snake finish finish workflow. It keeps the ont 2a umitools count stage tied to upstream `ont_2a_split_bam_by_strand` and the downstream handoff to `ont_2a_counts_to_sparse`. It tracks completion via `results/finish/ont_2a_umitools_count.done`.
metadata:
  workflow_id: mckellardw-slide_snake-finish
  workflow_name: mckellardw slide_snake finish
  step_id: ont_2a_umitools_count
  step_name: ont 2a umitools count
---

# Scope
Use this skill only for the `ont_2a_umitools_count` step in `mckellardw-slide_snake-finish`.

## Orchestration
- Upstream requirements: `ont_2a_split_bam_by_strand`
- Step file: `finish/mckellardw-slide_snake-finish/steps/ont_2a_umitools_count.smk`
- Config file: `finish/mckellardw-slide_snake-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/ont_2a_umitools_count.done`
- Representative outputs: `results/finish/ont_2a_umitools_count.done`
- Execution targets: `ont_2a_umitools_count`
- Downstream handoff: `ont_2a_counts_to_sparse`

## Guardrails
- Treat `results/finish/ont_2a_umitools_count.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/ont_2a_umitools_count.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `ont_2a_counts_to_sparse` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/ont_2a_umitools_count.done` exists and `ont_2a_counts_to_sparse` can proceed without re-running ont 2a umitools count.
