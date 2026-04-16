configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "split_sc_bam"


rule all:
  input:
    "results/finish/split_sc_bam.done"


rule run_split_sc_bam:
  output:
    "results/finish/split_sc_bam.done"
  run:
    run_step(STEP_ID, output[0])
