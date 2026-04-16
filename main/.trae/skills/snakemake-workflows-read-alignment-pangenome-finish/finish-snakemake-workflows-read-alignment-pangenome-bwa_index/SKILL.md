---
name: finish-snakemake-workflows-read-alignment-pangenome-bwa_index
description: Use this skill when orchestrating the retained "bwa_index" step of the snakemake workflows read alignment pangenome finish finish workflow. It keeps the bwa index stage tied to upstream `remove_iupac_codes` and the downstream handoff to `get_pangenome`. It tracks completion via `results/finish/bwa_index.done`.
metadata:
  workflow_id: read-alignment-pangenome-finish
  workflow_name: snakemake workflows read alignment pangenome finish
  step_id: bwa_index
  step_name: bwa index
---

# Scope
Use this skill only for the `bwa_index` step in `read-alignment-pangenome-finish`.

## Orchestration
- Upstream requirements: `remove_iupac_codes`
- Step file: `finish/read-alignment-pangenome-finish/steps/bwa_index.smk`
- Config file: `finish/read-alignment-pangenome-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/bwa_index.done`
- Representative outputs: `results/finish/bwa_index.done`
- Execution targets: `bwa_index`
- Downstream handoff: `get_pangenome`

## Guardrails
- Treat `results/finish/bwa_index.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/bwa_index.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `get_pangenome` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/bwa_index.done` exists and `get_pangenome` can proceed without re-running bwa index.
