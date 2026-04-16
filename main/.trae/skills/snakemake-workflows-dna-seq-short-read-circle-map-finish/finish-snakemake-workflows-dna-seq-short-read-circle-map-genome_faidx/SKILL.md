---
name: finish-snakemake-workflows-dna-seq-short-read-circle-map-genome_faidx
description: Use this skill when orchestrating the retained "genome_faidx" step of the snakemake workflows dna seq short read circle map finish finish workflow. It keeps the genome faidx stage tied to upstream `bwa_index` and the downstream handoff to `genome_dict`. It tracks completion via `results/finish/genome_faidx.done`.
metadata:
  workflow_id: dna-seq-short-read-circle-map-finish
  workflow_name: snakemake workflows dna seq short read circle map finish
  step_id: genome_faidx
  step_name: genome faidx
---

# Scope
Use this skill only for the `genome_faidx` step in `dna-seq-short-read-circle-map-finish`.

## Orchestration
- Upstream requirements: `bwa_index`
- Step file: `finish/dna-seq-short-read-circle-map-finish/steps/genome_faidx.smk`
- Config file: `finish/dna-seq-short-read-circle-map-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/genome_faidx.done`
- Representative outputs: `results/finish/genome_faidx.done`
- Execution targets: `genome_faidx`
- Downstream handoff: `genome_dict`

## Guardrails
- Treat `results/finish/genome_faidx.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/genome_faidx.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `genome_dict` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/genome_faidx.done` exists and `genome_dict` can proceed without re-running genome faidx.
