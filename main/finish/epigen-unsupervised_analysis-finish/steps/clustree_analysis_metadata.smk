configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "clustree_analysis_metadata"


rule all:
  input:
    "results/finish/clustree_analysis_metadata.done"


rule run_clustree_analysis_metadata:
  output:
    "results/finish/clustree_analysis_metadata.done"
  run:
    run_step(STEP_ID, output[0])
