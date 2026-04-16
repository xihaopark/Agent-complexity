configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "annotate"


rule all:
  input:
    "results/finish/annotate.done"


rule run_annotate:
  output:
    "results/finish/annotate.done"
  run:
    run_step(STEP_ID, output[0])
