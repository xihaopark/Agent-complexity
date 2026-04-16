---
name: finish-snakemake-workflows-dna-seq-neoantigen-prediction-make_sampleheader
description: Use this skill when orchestrating the retained "make_sampleheader" step of the snakemake workflows dna seq neoantigen prediction finish finish workflow. It keeps the make sampleheader stage tied to upstream `get_vep_plugins` and the downstream handoff to `map_reads`. It tracks completion via `results/finish/make_sampleheader.done`.
metadata:
  workflow_id: dna-seq-neoantigen-prediction-finish
  workflow_name: snakemake workflows dna seq neoantigen prediction finish
  step_id: make_sampleheader
  step_name: make sampleheader
---

# Scope
Use this skill only for the `make_sampleheader` step in `dna-seq-neoantigen-prediction-finish`.

## Orchestration
- Upstream requirements: `get_vep_plugins`
- Step file: `finish/dna-seq-neoantigen-prediction-finish/steps/make_sampleheader.smk`
- Config file: `finish/dna-seq-neoantigen-prediction-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/make_sampleheader.done`
- Representative outputs: `results/finish/make_sampleheader.done`
- Execution targets: `make_sampleheader`
- Downstream handoff: `map_reads`

## Guardrails
- Treat `results/finish/make_sampleheader.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/make_sampleheader.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `map_reads` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/make_sampleheader.done` exists and `map_reads` can proceed without re-running make sampleheader.
