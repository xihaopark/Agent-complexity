---
name: finish-snakemake-workflows-dna-seq-short-read-circle-map-datavzrd
description: Use this skill when orchestrating the retained "datavzrd" step of the snakemake workflows dna seq short read circle map finish finish workflow. It keeps the datavzrd stage tied to upstream `render_datavzrd_config` and the downstream handoff to `all`. It tracks completion via `results/finish/datavzrd.done`.
metadata:
  workflow_id: dna-seq-short-read-circle-map-finish
  workflow_name: snakemake workflows dna seq short read circle map finish
  step_id: datavzrd
  step_name: datavzrd
---

# Scope
Use this skill only for the `datavzrd` step in `dna-seq-short-read-circle-map-finish`.

## Orchestration
- Upstream requirements: `render_datavzrd_config`
- Step file: `finish/dna-seq-short-read-circle-map-finish/steps/datavzrd.smk`
- Config file: `finish/dna-seq-short-read-circle-map-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/datavzrd.done`
- Representative outputs: `results/finish/datavzrd.done`
- Execution targets: `datavzrd`
- Downstream handoff: `all`

## Guardrails
- Treat `results/finish/datavzrd.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/datavzrd.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `all` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/datavzrd.done` exists and `all` can proceed without re-running datavzrd.
