---
name: finish-snakemake-workflows-dna-seq-short-read-circle-map-render_datavzrd_config
description: Use this skill when orchestrating the retained "render_datavzrd_config" step of the snakemake workflows dna seq short read circle map finish finish workflow. It keeps the render datavzrd config stage tied to upstream `clean_circle_map_realign_output` and the downstream handoff to `datavzrd`. It tracks completion via `results/finish/render_datavzrd_config.done`.
metadata:
  workflow_id: dna-seq-short-read-circle-map-finish
  workflow_name: snakemake workflows dna seq short read circle map finish
  step_id: render_datavzrd_config
  step_name: render datavzrd config
---

# Scope
Use this skill only for the `render_datavzrd_config` step in `dna-seq-short-read-circle-map-finish`.

## Orchestration
- Upstream requirements: `clean_circle_map_realign_output`
- Step file: `finish/dna-seq-short-read-circle-map-finish/steps/render_datavzrd_config.smk`
- Config file: `finish/dna-seq-short-read-circle-map-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/render_datavzrd_config.done`
- Representative outputs: `results/finish/render_datavzrd_config.done`
- Execution targets: `render_datavzrd_config`
- Downstream handoff: `datavzrd`

## Guardrails
- Treat `results/finish/render_datavzrd_config.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/render_datavzrd_config.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `datavzrd` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/render_datavzrd_config.done` exists and `datavzrd` can proceed without re-running render datavzrd config.
