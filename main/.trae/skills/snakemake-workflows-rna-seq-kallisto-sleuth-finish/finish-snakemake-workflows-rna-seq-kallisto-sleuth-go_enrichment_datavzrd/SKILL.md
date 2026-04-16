---
name: finish-snakemake-workflows-rna-seq-kallisto-sleuth-go_enrichment_datavzrd
description: Use this skill when orchestrating the retained "go_enrichment_datavzrd" step of the snakemake workflows rna seq kallisto sleuth finish finish workflow. It keeps the go enrichment datavzrd stage tied to upstream `diffexp_datavzrd` and the downstream handoff to `meta_compare_datavzrd`. It tracks completion via `results/finish/go_enrichment_datavzrd.done`.
metadata:
  workflow_id: rna-seq-kallisto-sleuth-finish
  workflow_name: snakemake workflows rna seq kallisto sleuth finish
  step_id: go_enrichment_datavzrd
  step_name: go enrichment datavzrd
---

# Scope
Use this skill only for the `go_enrichment_datavzrd` step in `rna-seq-kallisto-sleuth-finish`.

## Orchestration
- Upstream requirements: `diffexp_datavzrd`
- Step file: `finish/rna-seq-kallisto-sleuth-finish/steps/go_enrichment_datavzrd.smk`
- Config file: `finish/rna-seq-kallisto-sleuth-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/go_enrichment_datavzrd.done`
- Representative outputs: `results/finish/go_enrichment_datavzrd.done`
- Execution targets: `go_enrichment_datavzrd`
- Downstream handoff: `meta_compare_datavzrd`

## Guardrails
- Treat `results/finish/go_enrichment_datavzrd.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/go_enrichment_datavzrd.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `meta_compare_datavzrd` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/go_enrichment_datavzrd.done` exists and `meta_compare_datavzrd` can proceed without re-running go enrichment datavzrd.
