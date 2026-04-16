configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "methylkit_split_mku2tibble"


rule all:
  input:
    "results/finish/methylkit_split_mku2tibble.done"


rule run_methylkit_split_mku2tibble:
  output:
    "results/finish/methylkit_split_mku2tibble.done"
  run:
    run_step(STEP_ID, output[0])
