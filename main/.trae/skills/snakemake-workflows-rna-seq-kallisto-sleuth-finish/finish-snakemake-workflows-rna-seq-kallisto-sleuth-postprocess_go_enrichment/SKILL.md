---
name: finish-snakemake-workflows-rna-seq-kallisto-sleuth-postprocess_go_enrichment
description: Use this skill when orchestrating the retained "postprocess_go_enrichment" step of the snakemake workflows rna seq kallisto sleuth finish finish workflow. It keeps the postprocess go enrichment stage tied to upstream `goatools_go_enrichment` and the downstream handoff to `postprocess_diffexp`. It tracks completion via `results/finish/postprocess_go_enrichment.done`.
metadata:
  workflow_id: rna-seq-kallisto-sleuth-finish
  workflow_name: snakemake workflows rna seq kallisto sleuth finish
  step_id: postprocess_go_enrichment
  step_name: postprocess go enrichment
---

# Scope
Use this skill only for the `postprocess_go_enrichment` step in `rna-seq-kallisto-sleuth-finish`.

## Orchestration
- Upstream requirements: `goatools_go_enrichment`
- Step file: `finish/rna-seq-kallisto-sleuth-finish/steps/postprocess_go_enrichment.smk`
- Config file: `finish/rna-seq-kallisto-sleuth-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/postprocess_go_enrichment.done`
- Representative outputs: `results/finish/postprocess_go_enrichment.done`
- Execution targets: `postprocess_go_enrichment`
- Downstream handoff: `postprocess_diffexp`

## Guardrails
- Treat `results/finish/postprocess_go_enrichment.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/postprocess_go_enrichment.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `postprocess_diffexp` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/postprocess_go_enrichment.done` exists and `postprocess_diffexp` can proceed without re-running postprocess go enrichment.
