configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "plotFingerprint"


rule all:
  input:
    "results/finish/plotFingerprint.done"


rule run_plotFingerprint:
  output:
    "results/finish/plotFingerprint.done"
  run:
    run_step(STEP_ID, output[0])
