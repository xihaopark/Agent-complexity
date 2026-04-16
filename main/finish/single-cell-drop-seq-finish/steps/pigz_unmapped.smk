configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "pigz_unmapped"


rule all:
  input:
    "results/finish/pigz_unmapped.done"


rule run_pigz_unmapped:
  output:
    "results/finish/pigz_unmapped.done"
  run:
    run_step(STEP_ID, output[0])
