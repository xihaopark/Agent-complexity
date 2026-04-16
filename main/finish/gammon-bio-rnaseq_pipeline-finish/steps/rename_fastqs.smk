configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "rename_fastqs"


rule all:
  input:
    "results/finish/rename_fastqs.done"


rule run_rename_fastqs:
  output:
    "results/finish/rename_fastqs.done"
  run:
    run_step(STEP_ID, output[0])
