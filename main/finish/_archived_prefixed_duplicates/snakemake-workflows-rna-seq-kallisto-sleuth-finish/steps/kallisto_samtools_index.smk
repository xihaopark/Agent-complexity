configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "kallisto_samtools_index"


rule all:
  input:
    "results/finish/kallisto_samtools_index.done"


rule run_kallisto_samtools_index:
  output:
    "results/finish/kallisto_samtools_index.done"
  run:
    run_step(STEP_ID, output[0])
