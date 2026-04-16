configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "binned_CDS_coverage"


rule all:
  input:
    "results/finish/binned_CDS_coverage.done"


rule run_binned_CDS_coverage:
  output:
    "results/finish/binned_CDS_coverage.done"
  run:
    run_step(STEP_ID, output[0])
