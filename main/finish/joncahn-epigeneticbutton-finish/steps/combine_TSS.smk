configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "combine_TSS"


rule all:
  input:
    "results/finish/combine_TSS.done"


rule run_combine_TSS:
  output:
    "results/finish/combine_TSS.done"
  run:
    run_step(STEP_ID, output[0])
