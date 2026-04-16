---
name: finish-snakemake-workflows-dna-seq-short-read-circle-map-genome_dict
description: Use this skill when orchestrating the retained "genome_dict" step of the snakemake workflows dna seq short read circle map finish finish workflow. It keeps the genome dict stage tied to upstream `genome_faidx` and the downstream handoff to `get_known_variants`. It tracks completion via `results/finish/genome_dict.done`.
metadata:
  workflow_id: dna-seq-short-read-circle-map-finish
  workflow_name: snakemake workflows dna seq short read circle map finish
  step_id: genome_dict
  step_name: genome dict
---

# Scope
Use this skill only for the `genome_dict` step in `dna-seq-short-read-circle-map-finish`.

## Orchestration
- Upstream requirements: `genome_faidx`
- Step file: `finish/dna-seq-short-read-circle-map-finish/steps/genome_dict.smk`
- Config file: `finish/dna-seq-short-read-circle-map-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/genome_dict.done`
- Representative outputs: `results/finish/genome_dict.done`
- Execution targets: `genome_dict`
- Downstream handoff: `get_known_variants`

## Guardrails
- Treat `results/finish/genome_dict.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/genome_dict.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `get_known_variants` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/genome_dict.done` exists and `get_known_variants` can proceed without re-running genome dict.
