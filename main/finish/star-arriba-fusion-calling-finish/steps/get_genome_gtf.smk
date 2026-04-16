configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "get_genome_gtf"


rule all:
  input:
    "results/finish/get_genome_gtf.done"


rule run_get_genome_gtf:
  output:
    "results/finish/get_genome_gtf.done"
  run:
    run_step(STEP_ID, output[0])
