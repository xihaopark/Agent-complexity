---
name: finish-snakemake-workflows-read-alignment-pangenome-bam_index
description: Use this skill when orchestrating the retained "bam_index" step of the snakemake workflows read alignment pangenome finish finish workflow. It keeps the bam index stage and the downstream handoff to `tabix_known_variants`. It tracks completion via `results/finish/bam_index.done`.
metadata:
  workflow_id: read-alignment-pangenome-finish
  workflow_name: snakemake workflows read alignment pangenome finish
  step_id: bam_index
  step_name: bam index
---

# Scope
Use this skill only for the `bam_index` step in `read-alignment-pangenome-finish`.

## Orchestration
- Upstream requirements: none
- Step file: `finish/read-alignment-pangenome-finish/steps/bam_index.smk`
- Config file: `finish/read-alignment-pangenome-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/bam_index.done`
- Representative outputs: `results/finish/bam_index.done`
- Execution targets: `bam_index`
- Downstream handoff: `tabix_known_variants`

## Guardrails
- Treat `results/finish/bam_index.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/bam_index.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `tabix_known_variants` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/bam_index.done` exists and `tabix_known_variants` can proceed without re-running bam index.
