configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "get_main_transcripts_fasta"


rule all:
  input:
    "results/finish/get_main_transcripts_fasta.done"


rule run_get_main_transcripts_fasta:
  output:
    "results/finish/get_main_transcripts_fasta.done"
  run:
    run_step(STEP_ID, output[0])
