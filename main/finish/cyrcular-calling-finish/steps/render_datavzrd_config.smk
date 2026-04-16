configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "render_datavzrd_config"


rule all:
  input:
    "results/finish/render_datavzrd_config.done"


rule run_render_datavzrd_config:
  output:
    "results/finish/render_datavzrd_config.done"
  run:
    run_step(STEP_ID, output[0])
