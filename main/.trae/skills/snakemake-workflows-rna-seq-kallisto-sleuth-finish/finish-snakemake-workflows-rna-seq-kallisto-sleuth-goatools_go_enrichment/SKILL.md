---
name: finish-snakemake-workflows-rna-seq-kallisto-sleuth-goatools_go_enrichment
description: Use this skill when orchestrating the retained "goatools_go_enrichment" step of the snakemake workflows rna seq kallisto sleuth finish finish workflow. It keeps the goatools go enrichment stage tied to upstream `download_go_obo` and the downstream handoff to `postprocess_go_enrichment`. It tracks completion via `results/finish/goatools_go_enrichment.done`.
metadata:
  workflow_id: rna-seq-kallisto-sleuth-finish
  workflow_name: snakemake workflows rna seq kallisto sleuth finish
  step_id: goatools_go_enrichment
  step_name: goatools go enrichment
---

# Scope
Use this skill only for the `goatools_go_enrichment` step in `rna-seq-kallisto-sleuth-finish`.

## Orchestration
- Upstream requirements: `download_go_obo`
- Step file: `finish/rna-seq-kallisto-sleuth-finish/steps/goatools_go_enrichment.smk`
- Config file: `finish/rna-seq-kallisto-sleuth-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/goatools_go_enrichment.done`
- Representative outputs: `results/finish/goatools_go_enrichment.done`
- Execution targets: `goatools_go_enrichment`
- Downstream handoff: `postprocess_go_enrichment`

## Guardrails
- Treat `results/finish/goatools_go_enrichment.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/goatools_go_enrichment.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `postprocess_go_enrichment` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/goatools_go_enrichment.done` exists and `postprocess_go_enrichment` can proceed without re-running goatools go enrichment.
