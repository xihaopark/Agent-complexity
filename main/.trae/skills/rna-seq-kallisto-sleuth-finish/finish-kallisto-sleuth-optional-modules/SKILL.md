---
name: finish-kallisto-sleuth-optional-modules
description: Use this skill when orchestrating the retained "optional_modules" step of the RNA-seq Kallisto Sleuth finish workflow. It frames the post-analysis optional comparison stage and preserves the handoff into the final delivery report.
metadata:
  workflow_id: rna-seq-kallisto-sleuth-finish
  workflow_name: RNA-seq Kallisto Sleuth Finish Workflow
  step_id: optional_modules
  step_name: Run optional comparison modules
---

# Scope
Use this skill only for the `optional_modules` step in `rna-seq-kallisto-sleuth-finish`.

## Orchestration
- Upstream requirements: `differential_expression`
- Step file: `finish/rna-seq-kallisto-sleuth-finish/steps/optional_modules.smk`
- Config file: `finish/rna-seq-kallisto-sleuth-finish/config_basic/config.yaml`
- Shared environment: `snakemake`
- Completion artifacts: `results/finish/optional_modules.done`
- Representative outputs: `results/finish/optional_modules.done`
- Downstream handoff: `delivery_report`

## Guardrails
- Treat `results/finish/optional_modules.done` as the authoritative completion signal for the wrapped finish step.
- This stage is config-sensitive; it may validly produce no extra business artifacts when optional analyses are disabled.

## Done Criteria
Mark this step complete only when optional module outputs exist for the configured comparisons and the delivery-report step can package them without rerunning analysis.
