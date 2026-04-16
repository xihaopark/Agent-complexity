configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "bamCoverage"


rule all:
  input:
    "results/finish/bamCoverage.done"


rule run_bamCoverage:
  output:
    "results/finish/bamCoverage.done"
  run:
    run_step(STEP_ID, output[0])
