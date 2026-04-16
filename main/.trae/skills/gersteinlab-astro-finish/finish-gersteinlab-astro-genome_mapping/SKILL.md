---
name: finish-gersteinlab-astro-genome_mapping
description: Use this skill when orchestrating the retained "genome_mapping" step of the gersteinlab astro finish finish workflow. It keeps the Genome Mapping stage tied to upstream `demultiplexing` and the downstream handoff to `feature_counting`. It tracks completion via `results/finish/genome_mapping.done`.
metadata:
  workflow_id: gersteinlab-astro-finish
  workflow_name: gersteinlab astro finish
  step_id: genome_mapping
  step_name: Genome Mapping
---

# Scope
Use this skill only for the `genome_mapping` step in `gersteinlab-astro-finish`.

## Orchestration
- Upstream requirements: `demultiplexing`
- Step file: `finish/gersteinlab-astro-finish/steps/genome_mapping.smk`
- Config file: `finish/gersteinlab-astro-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/genome_mapping.done`
- Representative outputs: `results/finish/genome_mapping.done`
- Execution targets: `genome_mapping`
- Downstream handoff: `feature_counting`

## Guardrails
- Treat `results/finish/genome_mapping.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/genome_mapping.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `feature_counting` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/genome_mapping.done` exists and `feature_counting` can proceed without re-running Genome Mapping.
