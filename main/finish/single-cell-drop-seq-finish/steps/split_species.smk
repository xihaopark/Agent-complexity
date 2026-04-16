configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "split_species"


rule all:
  input:
    "results/finish/split_species.done"


rule run_split_species:
  output:
    "results/finish/split_species.done"
  run:
    run_step(STEP_ID, output[0])
