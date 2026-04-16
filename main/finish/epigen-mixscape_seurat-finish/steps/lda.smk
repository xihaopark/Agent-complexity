configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "lda"


rule all:
  input:
    "results/finish/lda.done"


rule run_lda:
  output:
    "results/finish/lda.done"
  run:
    run_step(STEP_ID, output[0])
