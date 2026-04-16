---
name: finish-snakemake-workflows-rna-seq-kallisto-sleuth-meta_compare_enrichment
description: Use this skill when orchestrating the retained "meta_compare_enrichment" step of the snakemake workflows rna seq kallisto sleuth finish finish workflow. It keeps the meta compare enrichment stage tied to upstream `meta_compare_diffexp` and the downstream handoff to `meta_compare_pathways`. It tracks completion via `results/finish/meta_compare_enrichment.done`.
metadata:
  workflow_id: rna-seq-kallisto-sleuth-finish
  workflow_name: snakemake workflows rna seq kallisto sleuth finish
  step_id: meta_compare_enrichment
  step_name: meta compare enrichment
---

# Scope
Use this skill only for the `meta_compare_enrichment` step in `rna-seq-kallisto-sleuth-finish`.

## Orchestration
- Upstream requirements: `meta_compare_diffexp`
- Step file: `finish/rna-seq-kallisto-sleuth-finish/steps/meta_compare_enrichment.smk`
- Config file: `finish/rna-seq-kallisto-sleuth-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/meta_compare_enrichment.done`
- Representative outputs: `results/finish/meta_compare_enrichment.done`
- Execution targets: `meta_compare_enrichment`
- Downstream handoff: `meta_compare_pathways`

## Guardrails
- Treat `results/finish/meta_compare_enrichment.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/meta_compare_enrichment.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `meta_compare_pathways` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/meta_compare_enrichment.done` exists and `meta_compare_pathways` can proceed without re-running meta compare enrichment.
