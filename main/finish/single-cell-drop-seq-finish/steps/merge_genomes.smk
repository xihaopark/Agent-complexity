configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "merge_genomes"


rule all:
  input:
    "results/finish/merge_genomes.done"


rule run_merge_genomes:
  output:
    "results/finish/merge_genomes.done"
  run:
    run_step(STEP_ID, output[0])
