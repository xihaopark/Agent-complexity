configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "genome_to_transcriptome"


rule all:
  input:
    "results/finish/genome_to_transcriptome.done"


rule run_genome_to_transcriptome:
  output:
    "results/finish/genome_to_transcriptome.done"
  run:
    run_step(STEP_ID, output[0])
