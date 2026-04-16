---
name: finish-kallisto-sleuth-prepare-reads
description: Use this skill when orchestrating the retained "prepare_reads" step of the RNA-seq Kallisto Sleuth finish workflow. It keeps read preparation tied to prepared references and sets up the quantification stage with the expected staged read outputs.
metadata:
  workflow_id: rna-seq-kallisto-sleuth-finish
  workflow_name: RNA-seq Kallisto Sleuth Finish Workflow
  step_id: prepare_reads
  step_name: Prepare reads for quantification
---

# Scope
Use this skill only for the `prepare_reads` step in `rna-seq-kallisto-sleuth-finish`.

## Orchestration
- Upstream requirements: `prepare_references`
- Step file: `finish/rna-seq-kallisto-sleuth-finish/steps/prepare_reads.smk`
- Config file: `finish/rna-seq-kallisto-sleuth-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/prepare_reads.done`
- Representative outputs: `results/stats/max-read-length.json`
- Execution targets: `results/stats/max-read-length.json`
- Downstream handoff: `quantify`

## Guardrails
- Treat `results/finish/prepare_reads.done` as the authoritative completion signal for the wrapped finish step.
- Keep this step scoped to read trimming and read-length preparation outputs needed by quantification.

## Done Criteria
Mark this step complete only when the prepared read assets exist and the quantification step can proceed without revisiting reference generation.
