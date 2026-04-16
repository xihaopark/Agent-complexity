configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "clustree_analysis"


rule all:
  input:
    "results/finish/clustree_analysis.done"


rule run_clustree_analysis:
  output:
    "results/finish/clustree_analysis.done"
  run:
    run_step(STEP_ID, output[0])
