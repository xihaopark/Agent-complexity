---
name: finish-gersteinlab-astro-demultiplexing
description: Use this skill when orchestrating the retained "demultiplexing" step of the gersteinlab astro finish finish workflow. It keeps the Demultiplexing stage and the downstream handoff to `genome_mapping`. It tracks completion via `results/finish/demultiplexing.done`.
metadata:
  workflow_id: gersteinlab-astro-finish
  workflow_name: gersteinlab astro finish
  step_id: demultiplexing
  step_name: Demultiplexing
---

# Scope
Use this skill only for the `demultiplexing` step in `gersteinlab-astro-finish`.

## Orchestration
- Upstream requirements: none
- Step file: `finish/gersteinlab-astro-finish/steps/demultiplexing.smk`
- Config file: `finish/gersteinlab-astro-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/demultiplexing.done`
- Representative outputs: `results/finish/demultiplexing.done`
- Execution targets: `demultiplexing`
- Downstream handoff: `genome_mapping`

## Guardrails
- Treat `results/finish/demultiplexing.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/demultiplexing.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `genome_mapping` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/demultiplexing.done` exists and `genome_mapping` can proceed without re-running Demultiplexing.
