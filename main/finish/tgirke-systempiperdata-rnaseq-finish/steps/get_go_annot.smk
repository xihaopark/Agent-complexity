configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "get_go_annot"


rule all:
  input:
    "results/finish/get_go_annot.done"


rule run_get_go_annot:
  output:
    "results/finish/get_go_annot.done"
  run:
    run_step(STEP_ID, output[0])
