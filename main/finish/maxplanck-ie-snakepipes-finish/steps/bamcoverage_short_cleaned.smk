configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "bamcoverage_short_cleaned"


rule all:
  input:
    "results/finish/bamcoverage_short_cleaned.done"


rule run_bamcoverage_short_cleaned:
  output:
    "results/finish/bamcoverage_short_cleaned.done"
  run:
    run_step(STEP_ID, output[0])
