configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "do_counts"


rule all:
  input:
    "results/finish/do_counts.done"


rule run_do_counts:
  output:
    "results/finish/do_counts.done"
  run:
    run_step(STEP_ID, output[0])
