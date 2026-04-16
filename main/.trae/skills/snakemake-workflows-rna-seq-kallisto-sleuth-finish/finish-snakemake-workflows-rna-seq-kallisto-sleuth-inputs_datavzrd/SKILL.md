---
name: finish-snakemake-workflows-rna-seq-kallisto-sleuth-inputs_datavzrd
description: Use this skill when orchestrating the retained "inputs_datavzrd" step of the snakemake workflows rna seq kallisto sleuth finish finish workflow. It keeps the inputs datavzrd stage tied to upstream `meta_compare_datavzrd` and the downstream handoff to `bam_paired_to_fastq`. It tracks completion via `results/finish/inputs_datavzrd.done`.
metadata:
  workflow_id: rna-seq-kallisto-sleuth-finish
  workflow_name: snakemake workflows rna seq kallisto sleuth finish
  step_id: inputs_datavzrd
  step_name: inputs datavzrd
---

# Scope
Use this skill only for the `inputs_datavzrd` step in `rna-seq-kallisto-sleuth-finish`.

## Orchestration
- Upstream requirements: `meta_compare_datavzrd`
- Step file: `finish/rna-seq-kallisto-sleuth-finish/steps/inputs_datavzrd.smk`
- Config file: `finish/rna-seq-kallisto-sleuth-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/inputs_datavzrd.done`
- Representative outputs: `results/finish/inputs_datavzrd.done`
- Execution targets: `inputs_datavzrd`
- Downstream handoff: `bam_paired_to_fastq`

## Guardrails
- Treat `results/finish/inputs_datavzrd.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/inputs_datavzrd.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `bam_paired_to_fastq` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/inputs_datavzrd.done` exists and `bam_paired_to_fastq` can proceed without re-running inputs datavzrd.
