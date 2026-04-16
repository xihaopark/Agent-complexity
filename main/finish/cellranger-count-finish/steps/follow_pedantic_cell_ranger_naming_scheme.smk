configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "follow_pedantic_cell_ranger_naming_scheme"


rule all:
  input:
    "results/finish/follow_pedantic_cell_ranger_naming_scheme.done"


rule run_follow_pedantic_cell_ranger_naming_scheme:
  output:
    "results/finish/follow_pedantic_cell_ranger_naming_scheme.done"
  run:
    run_step(STEP_ID, output[0])
