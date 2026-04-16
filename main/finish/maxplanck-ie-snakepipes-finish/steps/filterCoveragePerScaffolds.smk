configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "filterCoveragePerScaffolds"


rule all:
  input:
    "results/finish/filterCoveragePerScaffolds.done"


rule run_filterCoveragePerScaffolds:
  output:
    "results/finish/filterCoveragePerScaffolds.done"
  run:
    run_step(STEP_ID, output[0])
