configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "bowtie2_index"


rule all:
  input:
    "results/finish/bowtie2_index.done"


rule run_bowtie2_index:
  output:
    "results/finish/bowtie2_index.done"
  run:
    run_step(STEP_ID, output[0])
