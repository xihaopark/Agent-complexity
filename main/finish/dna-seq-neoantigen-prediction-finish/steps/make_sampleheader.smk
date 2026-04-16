configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "make_sampleheader"


rule all:
  input:
    "results/finish/make_sampleheader.done"


rule run_make_sampleheader:
  output:
    "results/finish/make_sampleheader.done"
  run:
    run_step(STEP_ID, output[0])
