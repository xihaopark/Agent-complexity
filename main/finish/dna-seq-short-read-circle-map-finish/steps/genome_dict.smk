configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "genome_dict"


rule all:
  input:
    "results/finish/genome_dict.done"


rule run_genome_dict:
  output:
    "results/finish/genome_dict.done"
  run:
    run_step(STEP_ID, output[0])
