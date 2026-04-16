configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ont_2a_counts_to_sparse"


rule all:
  input:
    "results/finish/ont_2a_counts_to_sparse.done"


rule run_ont_2a_counts_to_sparse:
  output:
    "results/finish/ont_2a_counts_to_sparse.done"
  run:
    run_step(STEP_ID, output[0])
