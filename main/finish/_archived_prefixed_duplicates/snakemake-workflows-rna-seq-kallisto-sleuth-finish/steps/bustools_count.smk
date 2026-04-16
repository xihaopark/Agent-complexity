configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "bustools_count"


rule all:
  input:
    "results/finish/bustools_count.done"


rule run_bustools_count:
  output:
    "results/finish/bustools_count.done"
  run:
    run_step(STEP_ID, output[0])
