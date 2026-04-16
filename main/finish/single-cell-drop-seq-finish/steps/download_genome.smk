configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "download_genome"


rule all:
  input:
    "results/finish/download_genome.done"


rule run_download_genome:
  output:
    "results/finish/download_genome.done"
  run:
    run_step(STEP_ID, output[0])
