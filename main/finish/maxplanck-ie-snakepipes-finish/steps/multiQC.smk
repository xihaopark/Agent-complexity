configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "multiQC"


rule all:
  input:
    "results/finish/multiQC.done"


rule run_multiQC:
  output:
    "results/finish/multiQC.done"
  run:
    run_step(STEP_ID, output[0])
