---
name: finish-snakemake-workflows-rna-seq-kallisto-sleuth-spia_datavzrd
description: Use this skill when orchestrating the retained "spia_datavzrd" step of the snakemake workflows rna seq kallisto sleuth finish finish workflow. It keeps the spia datavzrd stage tied to upstream `plot_pathway_scatter` and the downstream handoff to `diffexp_datavzrd`. It tracks completion via `results/finish/spia_datavzrd.done`.
metadata:
  workflow_id: rna-seq-kallisto-sleuth-finish
  workflow_name: snakemake workflows rna seq kallisto sleuth finish
  step_id: spia_datavzrd
  step_name: spia datavzrd
---

# Scope
Use this skill only for the `spia_datavzrd` step in `rna-seq-kallisto-sleuth-finish`.

## Orchestration
- Upstream requirements: `plot_pathway_scatter`
- Step file: `finish/rna-seq-kallisto-sleuth-finish/steps/spia_datavzrd.smk`
- Config file: `finish/rna-seq-kallisto-sleuth-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/spia_datavzrd.done`
- Representative outputs: `results/finish/spia_datavzrd.done`
- Execution targets: `spia_datavzrd`
- Downstream handoff: `diffexp_datavzrd`

## Guardrails
- Treat `results/finish/spia_datavzrd.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/spia_datavzrd.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `diffexp_datavzrd` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/spia_datavzrd.done` exists and `diffexp_datavzrd` can proceed without re-running spia datavzrd.
