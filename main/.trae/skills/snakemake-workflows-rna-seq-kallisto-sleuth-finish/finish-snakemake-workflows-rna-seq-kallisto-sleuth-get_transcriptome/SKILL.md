---
name: finish-snakemake-workflows-rna-seq-kallisto-sleuth-get_transcriptome
description: Use this skill when orchestrating the retained "get_transcriptome" step of the snakemake workflows rna seq kallisto sleuth finish finish workflow. It keeps the get transcriptome stage tied to upstream `get_sample_QC_histogram` and the downstream handoff to `get_annotation`. It tracks completion via `results/finish/get_transcriptome.done`.
metadata:
  workflow_id: rna-seq-kallisto-sleuth-finish
  workflow_name: snakemake workflows rna seq kallisto sleuth finish
  step_id: get_transcriptome
  step_name: get transcriptome
---

# Scope
Use this skill only for the `get_transcriptome` step in `rna-seq-kallisto-sleuth-finish`.

## Orchestration
- Upstream requirements: `get_sample_QC_histogram`
- Step file: `finish/rna-seq-kallisto-sleuth-finish/steps/get_transcriptome.smk`
- Config file: `finish/rna-seq-kallisto-sleuth-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/get_transcriptome.done`
- Representative outputs: `results/finish/get_transcriptome.done`
- Execution targets: `get_transcriptome`
- Downstream handoff: `get_annotation`

## Guardrails
- Treat `results/finish/get_transcriptome.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/get_transcriptome.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `get_annotation` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/get_transcriptome.done` exists and `get_annotation` can proceed without re-running get transcriptome.
