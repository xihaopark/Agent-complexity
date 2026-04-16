configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "check_gtf"


rule all:
  input:
    "results/finish/check_gtf.done"


rule run_check_gtf:
  output:
    "results/finish/check_gtf.done"
  run:
    run_step(STEP_ID, output[0])
