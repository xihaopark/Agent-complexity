configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "qc_stats"


rule all:
  input:
    "results/finish/qc_stats.done"


rule run_qc_stats:
  output:
    "results/finish/qc_stats.done"
  run:
    run_step(STEP_ID, output[0])
