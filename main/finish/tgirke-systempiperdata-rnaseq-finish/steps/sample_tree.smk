configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "sample_tree"


rule all:
  input:
    "results/finish/sample_tree.done"


rule run_sample_tree:
  output:
    "results/finish/sample_tree.done"
  run:
    run_step(STEP_ID, output[0])
