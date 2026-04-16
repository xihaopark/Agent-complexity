configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "genome_faidx"


rule all:
  input:
    "results/finish/genome_faidx.done"


rule run_genome_faidx:
  output:
    "results/finish/genome_faidx.done"
  run:
    run_step(STEP_ID, output[0])
