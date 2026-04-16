configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "plotFingerprint_allelic"


rule all:
  input:
    "results/finish/plotFingerprint_allelic.done"


rule run_plotFingerprint_allelic:
  output:
    "results/finish/plotFingerprint_allelic.done"
  run:
    run_step(STEP_ID, output[0])
