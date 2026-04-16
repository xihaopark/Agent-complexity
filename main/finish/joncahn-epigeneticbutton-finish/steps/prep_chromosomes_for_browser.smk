configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "prep_chromosomes_for_browser"


rule all:
  input:
    "results/finish/prep_chromosomes_for_browser.done"


rule run_prep_chromosomes_for_browser:
  output:
    "results/finish/prep_chromosomes_for_browser.done"
  run:
    run_step(STEP_ID, output[0])
