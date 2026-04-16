configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "fix_tag"


rule all:
  input:
    "results/finish/fix_tag.done"


rule run_fix_tag:
  output:
    "results/finish/fix_tag.done"
  run:
    run_step(STEP_ID, output[0])
