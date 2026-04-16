configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "meta_compare_datavzrd"


rule all:
  input:
    "results/finish/meta_compare_datavzrd.done"


rule run_meta_compare_datavzrd:
  output:
    "results/finish/meta_compare_datavzrd.done"
  run:
    run_step(STEP_ID, output[0])
