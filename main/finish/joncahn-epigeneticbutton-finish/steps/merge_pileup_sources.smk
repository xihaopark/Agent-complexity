configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "merge_pileup_sources"


rule all:
  input:
    "results/finish/merge_pileup_sources.done"


rule run_merge_pileup_sources:
  output:
    "results/finish/merge_pileup_sources.done"
  run:
    run_step(STEP_ID, output[0])
