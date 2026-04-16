configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "make_latex_tables"


rule all:
  input:
    "results/finish/make_latex_tables.done"


rule run_make_latex_tables:
  output:
    "results/finish/make_latex_tables.done"
  run:
    run_step(STEP_ID, output[0])
