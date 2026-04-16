configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "merge_trimmed_fastqs"


rule all:
  input:
    "results/finish/merge_trimmed_fastqs.done"


rule run_merge_trimmed_fastqs:
  output:
    "results/finish/merge_trimmed_fastqs.done"
  run:
    run_step(STEP_ID, output[0])
