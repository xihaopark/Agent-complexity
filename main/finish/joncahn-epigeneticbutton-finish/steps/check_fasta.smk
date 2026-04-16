configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "check_fasta"


rule all:
  input:
    "results/finish/check_fasta.done"


rule run_check_fasta:
  output:
    "results/finish/check_fasta.done"
  run:
    run_step(STEP_ID, output[0])
