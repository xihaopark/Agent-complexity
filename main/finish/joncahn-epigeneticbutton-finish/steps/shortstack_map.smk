configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "shortstack_map"


rule all:
  input:
    "results/finish/shortstack_map.done"


rule run_shortstack_map:
  output:
    "results/finish/shortstack_map.done"
  run:
    run_step(STEP_ID, output[0])
