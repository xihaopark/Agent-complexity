configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "build_splici_transcriptome"


rule all:
  input:
    "results/finish/build_splici_transcriptome.done"


rule run_build_splici_transcriptome:
  output:
    "results/finish/build_splici_transcriptome.done"
  run:
    run_step(STEP_ID, output[0])
