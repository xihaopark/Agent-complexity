---
name: finish-snakemake-workflows-rna-seq-kallisto-sleuth-meta_compare_pathways
description: Use this skill when orchestrating the retained "meta_compare_pathways" step of the snakemake workflows rna seq kallisto sleuth finish finish workflow. It keeps the meta compare pathways stage tied to upstream `meta_compare_enrichment` and the downstream handoff to `all`. It tracks completion via `results/finish/meta_compare_pathways.done`.
metadata:
  workflow_id: rna-seq-kallisto-sleuth-finish
  workflow_name: snakemake workflows rna seq kallisto sleuth finish
  step_id: meta_compare_pathways
  step_name: meta compare pathways
---

# Scope
Use this skill only for the `meta_compare_pathways` step in `rna-seq-kallisto-sleuth-finish`.

## Orchestration
- Upstream requirements: `meta_compare_enrichment`
- Step file: `finish/rna-seq-kallisto-sleuth-finish/steps/meta_compare_pathways.smk`
- Config file: `finish/rna-seq-kallisto-sleuth-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/meta_compare_pathways.done`
- Representative outputs: `results/finish/meta_compare_pathways.done`
- Execution targets: `meta_compare_pathways`
- Downstream handoff: `all`

## Guardrails
- Treat `results/finish/meta_compare_pathways.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/meta_compare_pathways.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `all` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/meta_compare_pathways.done` exists and `all` can proceed without re-running meta compare pathways.
