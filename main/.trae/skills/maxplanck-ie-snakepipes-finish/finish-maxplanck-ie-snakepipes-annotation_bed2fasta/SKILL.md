---
name: finish-maxplanck-ie-snakepipes-annotation_bed2fasta
description: Use this skill when orchestrating the retained "annotation_bed2fasta" step of the maxplanck ie snakepipes finish finish workflow. It keeps the annotation bed2fasta stage tied to upstream `gtf_to_files` and the downstream handoff to `all`. It tracks completion via `results/finish/annotation_bed2fasta.done`.
metadata:
  workflow_id: maxplanck-ie-snakepipes-finish
  workflow_name: maxplanck ie snakepipes finish
  step_id: annotation_bed2fasta
  step_name: annotation bed2fasta
---

# Scope
Use this skill only for the `annotation_bed2fasta` step in `maxplanck-ie-snakepipes-finish`.

## Orchestration
- Upstream requirements: `gtf_to_files`
- Step file: `finish/maxplanck-ie-snakepipes-finish/steps/annotation_bed2fasta.smk`
- Config file: `finish/maxplanck-ie-snakepipes-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/annotation_bed2fasta.done`
- Representative outputs: `results/finish/annotation_bed2fasta.done`
- Execution targets: `annotation_bed2fasta`
- Downstream handoff: `all`

## Guardrails
- Treat `results/finish/annotation_bed2fasta.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/annotation_bed2fasta.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `all` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/annotation_bed2fasta.done` exists and `all` can proceed without re-running annotation bed2fasta.
