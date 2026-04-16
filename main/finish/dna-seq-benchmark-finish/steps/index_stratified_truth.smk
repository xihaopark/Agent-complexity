configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "index_stratified_truth"


rule all:
  input:
    "results/finish/index_stratified_truth.done"


rule run_index_stratified_truth:
  output:
    "results/finish/index_stratified_truth.done"
  run:
    run_step(STEP_ID, output[0])
