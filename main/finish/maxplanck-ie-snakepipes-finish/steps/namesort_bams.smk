configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "namesort_bams"


rule all:
  input:
    "results/finish/namesort_bams.done"


rule run_namesort_bams:
  output:
    "results/finish/namesort_bams.done"
  run:
    run_step(STEP_ID, output[0])
