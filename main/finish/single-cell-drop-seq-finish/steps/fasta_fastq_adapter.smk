configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "fasta_fastq_adapter"


rule all:
  input:
    "results/finish/fasta_fastq_adapter.done"


rule run_fasta_fastq_adapter:
  output:
    "results/finish/fasta_fastq_adapter.done"
  run:
    run_step(STEP_ID, output[0])
