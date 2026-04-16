configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "render_scenario"


rule all:
  input:
    "results/finish/render_scenario.done"


rule run_render_scenario:
  output:
    "results/finish/render_scenario.done"
  run:
    run_step(STEP_ID, output[0])
