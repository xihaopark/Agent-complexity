---
name: finish-snakemake-workflows-dna-seq-short-read-circle-map-clean_circle_map_realign_output
description: Use this skill when orchestrating the retained "clean_circle_map_realign_output" step of the snakemake workflows dna seq short read circle map finish finish workflow. It keeps the clean circle map realign output stage tied to upstream `circle_map_realign` and the downstream handoff to `render_datavzrd_config`. It tracks completion via `results/finish/clean_circle_map_realign_output.done`.
metadata:
  workflow_id: dna-seq-short-read-circle-map-finish
  workflow_name: snakemake workflows dna seq short read circle map finish
  step_id: clean_circle_map_realign_output
  step_name: clean circle map realign output
---

# Scope
Use this skill only for the `clean_circle_map_realign_output` step in `dna-seq-short-read-circle-map-finish`.

## Orchestration
- Upstream requirements: `circle_map_realign`
- Step file: `finish/dna-seq-short-read-circle-map-finish/steps/clean_circle_map_realign_output.smk`
- Config file: `finish/dna-seq-short-read-circle-map-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/clean_circle_map_realign_output.done`
- Representative outputs: `results/finish/clean_circle_map_realign_output.done`
- Execution targets: `clean_circle_map_realign_output`
- Downstream handoff: `render_datavzrd_config`

## Guardrails
- Treat `results/finish/clean_circle_map_realign_output.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/clean_circle_map_realign_output.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `render_datavzrd_config` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/clean_circle_map_realign_output.done` exists and `render_datavzrd_config` can proceed without re-running clean circle map realign output.
