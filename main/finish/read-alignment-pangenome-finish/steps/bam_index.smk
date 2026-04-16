configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "bam_index"


rule all:
  input:
    "results/finish/bam_index.done"


rule run_bam_index:
  output:
    "results/finish/bam_index.done"
  run:
    run_step(STEP_ID, output[0])
