---
name: finish-joncahn-epigeneticbutton-call_all_degs
description: Use this skill when orchestrating the retained "call_all_DEGs" step of the joncahn epigeneticbutton finish finish workflow. It keeps the call all DEGs stage tied to upstream `prep_files_for_DEGs` and the downstream handoff to `gather_gene_expression_rpkm`. It tracks completion via `results/finish/call_all_DEGs.done`.
metadata:
  workflow_id: joncahn-epigeneticbutton-finish
  workflow_name: joncahn epigeneticbutton finish
  step_id: call_all_DEGs
  step_name: call all DEGs
---

# Scope
Use this skill only for the `call_all_DEGs` step in `joncahn-epigeneticbutton-finish`.

## Orchestration
- Upstream requirements: `prep_files_for_DEGs`
- Step file: `finish/joncahn-epigeneticbutton-finish/steps/call_all_DEGs.smk`
- Config file: `finish/joncahn-epigeneticbutton-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/call_all_DEGs.done`
- Representative outputs: `results/finish/call_all_DEGs.done`
- Execution targets: `call_all_DEGs`
- Downstream handoff: `gather_gene_expression_rpkm`

## Guardrails
- Treat `results/finish/call_all_DEGs.done` as the authoritative completion signal for this wrapped finish step.
- Keep this stage bounded to `steps/call_all_DEGs.smk` so the step remains separable and replayable inside the finish workflow.
- Preserve the downstream contract so `gather_gene_expression_rpkm` can start without recomputing this stage.

## Done Criteria
Mark this step complete only when `results/finish/call_all_DEGs.done` exists and `gather_gene_expression_rpkm` can proceed without re-running call all DEGs.
