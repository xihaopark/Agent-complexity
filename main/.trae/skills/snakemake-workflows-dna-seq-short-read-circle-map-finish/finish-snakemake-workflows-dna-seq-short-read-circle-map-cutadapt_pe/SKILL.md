---
name: finish-snakemake-workflows-dna-seq-short-read-circle-map-cutadapt_pe
description: Use this skill when orchestrating the retained "cutadapt_pe" step of the snakemake workflows dna seq short read circle map finish finish workflow. It keeps the cutadapt pe stage tied to upstream `tabix_known_variants` and the downstream handoff to `bwa_mem`. It tracks completion via `results/finish/cutadapt_pe.done`.
metadata:
  workflow_id: dna-seq-short-read-circle-map-finish
  workflow_name: snakemake workflows dna seq short read circle map finish
  step_id: cutadapt_pe
  step_name: cutadapt pe
---

# Scope
Use this skill only for the `cutadapt_pe` step in `dna-seq-short-read-circle-map-finish`.

## Orchestration
- Upstream requirements: `tabix_known_variants`
- Step file: `finish/dna-seq-short-read-circle-map-finish/steps/cutadapt_pe.smk`
- Config file: `finish/dna-seq-short-read-circle-map-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/cutadapt_pe.done`
- Representative outputs: `results/finish/cutadapt_pe.done`
- Execution targets: `cutadapt_pe`
- Downstream handoff: `bwa_mem`

## Guardrails
- Treat `results/finish/cutadapt_pe.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/cutadapt_pe.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `bwa_mem` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/cutadapt_pe.done` exists and `bwa_mem` can proceed without re-running cutadapt pe.
