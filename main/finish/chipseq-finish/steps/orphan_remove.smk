configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "orphan_remove"


rule all:
  input:
    "results/finish/orphan_remove.done"


rule run_orphan_remove:
  output:
    "results/finish/orphan_remove.done"
  run:
    run_step(STEP_ID, output[0])
