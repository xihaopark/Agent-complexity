configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "draw_fusions"


rule all:
  input:
    "results/finish/draw_fusions.done"


rule run_draw_fusions:
  output:
    "results/finish/draw_fusions.done"
  run:
    run_step(STEP_ID, output[0])
