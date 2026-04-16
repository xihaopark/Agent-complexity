configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "get_reference_genome"


rule all:
  input:
    "results/finish/get_reference_genome.done"


rule run_get_reference_genome:
  output:
    "results/finish/get_reference_genome.done"
  run:
    run_step(STEP_ID, output[0])
