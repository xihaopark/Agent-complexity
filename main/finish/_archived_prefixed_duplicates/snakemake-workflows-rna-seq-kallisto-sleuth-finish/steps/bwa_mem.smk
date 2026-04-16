configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "bwa_mem"


rule all:
  input:
    "results/finish/bwa_mem.done"


rule run_bwa_mem:
  output:
    "results/finish/bwa_mem.done"
  run:
    run_step(STEP_ID, output[0])
