configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "make_bowtie1_indices_large"


rule all:
  input:
    "results/finish/make_bowtie1_indices_large.done"


rule run_make_bowtie1_indices_large:
  output:
    "results/finish/make_bowtie1_indices_large.done"
  run:
    run_step(STEP_ID, output[0])
