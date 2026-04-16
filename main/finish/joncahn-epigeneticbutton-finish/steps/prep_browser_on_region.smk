configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "prep_browser_on_region"


rule all:
  input:
    "results/finish/prep_browser_on_region.done"


rule run_prep_browser_on_region:
  output:
    "results/finish/prep_browser_on_region.done"
  run:
    run_step(STEP_ID, output[0])
