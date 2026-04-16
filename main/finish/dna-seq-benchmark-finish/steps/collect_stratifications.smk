configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "collect_stratifications"


rule all:
  input:
    "results/finish/collect_stratifications.done"


rule run_collect_stratifications:
  output:
    "results/finish/collect_stratifications.done"
  run:
    run_step(STEP_ID, output[0])
