configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "merge_msi_results"


rule all:
  input:
    "results/finish/merge_msi_results.done"


rule run_merge_msi_results:
  output:
    "results/finish/merge_msi_results.done"
  run:
    run_step(STEP_ID, output[0])
