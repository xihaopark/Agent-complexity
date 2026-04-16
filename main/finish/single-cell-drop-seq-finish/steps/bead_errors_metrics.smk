configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "bead_errors_metrics"


rule all:
  input:
    "results/finish/bead_errors_metrics.done"


rule run_bead_errors_metrics:
  output:
    "results/finish/bead_errors_metrics.done"
  run:
    run_step(STEP_ID, output[0])
