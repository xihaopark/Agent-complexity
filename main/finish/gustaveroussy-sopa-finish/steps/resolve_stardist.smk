configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "resolve_stardist"


rule all:
  input:
    "results/finish/resolve_stardist.done"


rule run_resolve_stardist:
  output:
    "results/finish/resolve_stardist.done"
  run:
    run_step(STEP_ID, output[0])
