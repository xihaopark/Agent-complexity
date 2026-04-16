configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "homer_annotatepeaks"


rule all:
  input:
    "results/finish/homer_annotatepeaks.done"


rule run_homer_annotatepeaks:
  output:
    "results/finish/homer_annotatepeaks.done"
  run:
    run_step(STEP_ID, output[0])
