configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "genome_mapping"


rule all:
  input:
    "results/finish/genome_mapping.done"


rule run_genome_mapping:
  output:
    "results/finish/genome_mapping.done"
  run:
    run_step(STEP_ID, output[0])
