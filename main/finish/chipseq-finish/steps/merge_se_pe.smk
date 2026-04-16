configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "merge_se_pe"


rule all:
  input:
    "results/finish/merge_se_pe.done"


rule run_merge_se_pe:
  output:
    "results/finish/merge_se_pe.done"
  run:
    run_step(STEP_ID, output[0])
