configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "merge_bool_and_annotatepeaks"


rule all:
  input:
    "results/finish/merge_bool_and_annotatepeaks.done"


rule run_merge_bool_and_annotatepeaks:
  output:
    "results/finish/merge_bool_and_annotatepeaks.done"
  run:
    run_step(STEP_ID, output[0])
