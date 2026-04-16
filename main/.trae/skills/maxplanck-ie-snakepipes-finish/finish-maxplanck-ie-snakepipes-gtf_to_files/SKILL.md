---
name: finish-maxplanck-ie-snakepipes-gtf_to_files
description: Use this skill when orchestrating the retained "gtf_to_files" step of the maxplanck ie snakepipes finish finish workflow. It keeps the gtf to files stage tied to upstream `filter_gtf` and the downstream handoff to `annotation_bed2fasta`. It tracks completion via `results/finish/gtf_to_files.done`.
metadata:
  workflow_id: maxplanck-ie-snakepipes-finish
  workflow_name: maxplanck ie snakepipes finish
  step_id: gtf_to_files
  step_name: gtf to files
---

# Scope
Use this skill only for the `gtf_to_files` step in `maxplanck-ie-snakepipes-finish`.

## Orchestration
- Upstream requirements: `filter_gtf`
- Step file: `finish/maxplanck-ie-snakepipes-finish/steps/gtf_to_files.smk`
- Config file: `finish/maxplanck-ie-snakepipes-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/gtf_to_files.done`
- Representative outputs: `results/finish/gtf_to_files.done`
- Execution targets: `gtf_to_files`
- Downstream handoff: `annotation_bed2fasta`

## Guardrails
- Treat `results/finish/gtf_to_files.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/gtf_to_files.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `annotation_bed2fasta` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/gtf_to_files.done` exists and `annotation_bed2fasta` can proceed without re-running gtf to files.
