configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "tss_coverage"


rule all:
  input:
    "results/finish/tss_coverage.done"


rule run_tss_coverage:
  output:
    "results/finish/tss_coverage.done"
  run:
    run_step(STEP_ID, output[0])
