configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "diffexp_datavzrd"


rule all:
  input:
    "results/finish/diffexp_datavzrd.done"


rule run_diffexp_datavzrd:
  output:
    "results/finish/diffexp_datavzrd.done"
  run:
    run_step(STEP_ID, output[0])
