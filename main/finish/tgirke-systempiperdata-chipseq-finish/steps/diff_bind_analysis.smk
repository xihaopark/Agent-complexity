configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "diff_bind_analysis"


rule all:
  input:
    "results/finish/diff_bind_analysis.done"


rule run_diff_bind_analysis:
  output:
    "results/finish/diff_bind_analysis.done"
  run:
    run_step(STEP_ID, output[0])
