configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "build_flair_genome_index"


rule all:
  input:
    "results/finish/build_flair_genome_index.done"


rule run_build_flair_genome_index:
  output:
    "results/finish/build_flair_genome_index.done"
  run:
    run_step(STEP_ID, output[0])
