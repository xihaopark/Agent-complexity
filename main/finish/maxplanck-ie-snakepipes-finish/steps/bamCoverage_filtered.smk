configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "bamCoverage_filtered"


rule all:
  input:
    "results/finish/bamCoverage_filtered.done"


rule run_bamCoverage_filtered:
  output:
    "results/finish/bamCoverage_filtered.done"
  run:
    run_step(STEP_ID, output[0])
