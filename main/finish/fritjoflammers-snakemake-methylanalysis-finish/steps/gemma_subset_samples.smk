configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "gemma_subset_samples"


rule all:
  input:
    "results/finish/gemma_subset_samples.done"


rule run_gemma_subset_samples:
  output:
    "results/finish/gemma_subset_samples.done"
  run:
    run_step(STEP_ID, output[0])
