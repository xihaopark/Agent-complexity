---
name: finish-snakemake-workflows-rna-seq-kallisto-sleuth-diffexp_datavzrd
description: Use this skill when orchestrating the retained "diffexp_datavzrd" step of the snakemake workflows rna seq kallisto sleuth finish finish workflow. It keeps the diffexp datavzrd stage tied to upstream `spia_datavzrd` and the downstream handoff to `go_enrichment_datavzrd`. It tracks completion via `results/finish/diffexp_datavzrd.done`.
metadata:
  workflow_id: rna-seq-kallisto-sleuth-finish
  workflow_name: snakemake workflows rna seq kallisto sleuth finish
  step_id: diffexp_datavzrd
  step_name: diffexp datavzrd
---

# Scope
Use this skill only for the `diffexp_datavzrd` step in `rna-seq-kallisto-sleuth-finish`.

## Orchestration
- Upstream requirements: `spia_datavzrd`
- Step file: `finish/rna-seq-kallisto-sleuth-finish/steps/diffexp_datavzrd.smk`
- Config file: `finish/rna-seq-kallisto-sleuth-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/diffexp_datavzrd.done`
- Representative outputs: `results/finish/diffexp_datavzrd.done`
- Execution targets: `diffexp_datavzrd`
- Downstream handoff: `go_enrichment_datavzrd`

## Guardrails
- Treat `results/finish/diffexp_datavzrd.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/diffexp_datavzrd.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `go_enrichment_datavzrd` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/diffexp_datavzrd.done` exists and `go_enrichment_datavzrd` can proceed without re-running diffexp datavzrd.
