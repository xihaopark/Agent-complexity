configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "transcriptid_to_gene"


rule all:
  input:
    "results/finish/transcriptid_to_gene.done"


rule run_transcriptid_to_gene:
  output:
    "results/finish/transcriptid_to_gene.done"
  run:
    run_step(STEP_ID, output[0])
