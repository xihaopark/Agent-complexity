---
name: finish-snakemake-workflows-dna-seq-neoantigen-prediction-map_reads
description: Use this skill when orchestrating the retained "map_reads" step of the snakemake workflows dna seq neoantigen prediction finish finish workflow. It keeps the map reads stage tied to upstream `make_sampleheader` and the downstream handoff to `mark_duplicates`. It tracks completion via `results/finish/map_reads.done`.
metadata:
  workflow_id: dna-seq-neoantigen-prediction-finish
  workflow_name: snakemake workflows dna seq neoantigen prediction finish
  step_id: map_reads
  step_name: map reads
---

# Scope
Use this skill only for the `map_reads` step in `dna-seq-neoantigen-prediction-finish`.

## Orchestration
- Upstream requirements: `make_sampleheader`
- Step file: `finish/dna-seq-neoantigen-prediction-finish/steps/map_reads.smk`
- Config file: `finish/dna-seq-neoantigen-prediction-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/map_reads.done`
- Representative outputs: `results/finish/map_reads.done`
- Execution targets: `map_reads`
- Downstream handoff: `mark_duplicates`

## Guardrails
- Treat `results/finish/map_reads.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/map_reads.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `mark_duplicates` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/map_reads.done` exists and `mark_duplicates` can proceed without re-running map reads.
