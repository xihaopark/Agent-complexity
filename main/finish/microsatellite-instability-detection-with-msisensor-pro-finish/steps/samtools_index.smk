configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "samtools_index"


rule all:
  input:
    "results/finish/samtools_index.done"


rule run_samtools_index:
  output:
    "results/finish/samtools_index.done"
  run:
    run_step(STEP_ID, output[0])
