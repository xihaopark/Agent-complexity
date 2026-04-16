configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "rename_genome"


rule all:
  input:
    "results/finish/rename_genome.done"


rule run_rename_genome:
  output:
    "results/finish/rename_genome.done"
  run:
    run_step(STEP_ID, output[0])
