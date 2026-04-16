---
name: finish-snakemake-workflows-dna-seq-short-read-circle-map-bwa_mem
description: Use this skill when orchestrating the retained "bwa_mem" step of the snakemake workflows dna seq short read circle map finish finish workflow. It keeps the bwa mem stage tied to upstream `cutadapt_pe` and the downstream handoff to `merge_unit_bams_per_sample`. It tracks completion via `results/finish/bwa_mem.done`.
metadata:
  workflow_id: dna-seq-short-read-circle-map-finish
  workflow_name: snakemake workflows dna seq short read circle map finish
  step_id: bwa_mem
  step_name: bwa mem
---

# Scope
Use this skill only for the `bwa_mem` step in `dna-seq-short-read-circle-map-finish`.

## Orchestration
- Upstream requirements: `cutadapt_pe`
- Step file: `finish/dna-seq-short-read-circle-map-finish/steps/bwa_mem.smk`
- Config file: `finish/dna-seq-short-read-circle-map-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/bwa_mem.done`
- Representative outputs: `results/finish/bwa_mem.done`
- Execution targets: `bwa_mem`
- Downstream handoff: `merge_unit_bams_per_sample`

## Guardrails
- Treat `results/finish/bwa_mem.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/bwa_mem.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `merge_unit_bams_per_sample` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/bwa_mem.done` exists and `merge_unit_bams_per_sample` can proceed without re-running bwa mem.
