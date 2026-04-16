configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "one_vs_all_contrasts"


rule all:
  input:
    "results/finish/one_vs_all_contrasts.done"


rule run_one_vs_all_contrasts:
  output:
    "results/finish/one_vs_all_contrasts.done"
  run:
    run_step(STEP_ID, output[0])
