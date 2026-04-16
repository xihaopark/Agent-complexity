configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "datavzrd_methylkit_unite"


rule all:
  input:
    "results/finish/datavzrd_methylkit_unite.done"


rule run_datavzrd_methylkit_unite:
  output:
    "results/finish/datavzrd_methylkit_unite.done"
  run:
    run_step(STEP_ID, output[0])
