---
name: finish-snakemake-workflows-rna-seq-kallisto-sleuth-meta_compare_datavzrd
description: Use this skill when orchestrating the retained "meta_compare_datavzrd" step of the snakemake workflows rna seq kallisto sleuth finish finish workflow. It keeps the meta compare datavzrd stage tied to upstream `go_enrichment_datavzrd` and the downstream handoff to `inputs_datavzrd`. It tracks completion via `results/finish/meta_compare_datavzrd.done`.
metadata:
  workflow_id: rna-seq-kallisto-sleuth-finish
  workflow_name: snakemake workflows rna seq kallisto sleuth finish
  step_id: meta_compare_datavzrd
  step_name: meta compare datavzrd
---

# Scope
Use this skill only for the `meta_compare_datavzrd` step in `rna-seq-kallisto-sleuth-finish`.

## Orchestration
- Upstream requirements: `go_enrichment_datavzrd`
- Step file: `finish/rna-seq-kallisto-sleuth-finish/steps/meta_compare_datavzrd.smk`
- Config file: `finish/rna-seq-kallisto-sleuth-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/meta_compare_datavzrd.done`
- Representative outputs: `results/finish/meta_compare_datavzrd.done`
- Execution targets: `meta_compare_datavzrd`
- Downstream handoff: `inputs_datavzrd`

## Guardrails
- Treat `results/finish/meta_compare_datavzrd.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/meta_compare_datavzrd.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `inputs_datavzrd` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/meta_compare_datavzrd.done` exists and `inputs_datavzrd` can proceed without re-running meta compare datavzrd.
