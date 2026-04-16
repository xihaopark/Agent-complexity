configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "get_transcriptome"


rule all:
  input:
    "results/finish/get_transcriptome.done"


rule run_get_transcriptome:
  output:
    "results/finish/get_transcriptome.done"
  run:
    run_step(STEP_ID, output[0])
