configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "correct_transcriptome"


rule all:
  input:
    "results/finish/correct_transcriptome.done"


rule run_correct_transcriptome:
  output:
    "results/finish/correct_transcriptome.done"
  run:
    run_step(STEP_ID, output[0])
