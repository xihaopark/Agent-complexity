---
name: finish-snakemake-workflows-rna-seq-kallisto-sleuth-meta_compare_diffexp
description: Use this skill when orchestrating the retained "meta_compare_diffexp" step of the snakemake workflows rna seq kallisto sleuth finish finish workflow. It keeps the meta compare diffexp stage tied to upstream `bam_single_to_fastq` and the downstream handoff to `meta_compare_enrichment`. It tracks completion via `results/finish/meta_compare_diffexp.done`.
metadata:
  workflow_id: rna-seq-kallisto-sleuth-finish
  workflow_name: snakemake workflows rna seq kallisto sleuth finish
  step_id: meta_compare_diffexp
  step_name: meta compare diffexp
---

# Scope
Use this skill only for the `meta_compare_diffexp` step in `rna-seq-kallisto-sleuth-finish`.

## Orchestration
- Upstream requirements: `bam_single_to_fastq`
- Step file: `finish/rna-seq-kallisto-sleuth-finish/steps/meta_compare_diffexp.smk`
- Config file: `finish/rna-seq-kallisto-sleuth-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/meta_compare_diffexp.done`
- Representative outputs: `results/finish/meta_compare_diffexp.done`
- Execution targets: `meta_compare_diffexp`
- Downstream handoff: `meta_compare_enrichment`

## Guardrails
- Treat `results/finish/meta_compare_diffexp.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/meta_compare_diffexp.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `meta_compare_enrichment` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/meta_compare_diffexp.done` exists and `meta_compare_enrichment` can proceed without re-running meta compare diffexp.
