configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "fasta_index"


rule all:
  input:
    "results/finish/fasta_index.done"


rule run_fasta_index:
  output:
    "results/finish/fasta_index.done"
  run:
    run_step(STEP_ID, output[0])
