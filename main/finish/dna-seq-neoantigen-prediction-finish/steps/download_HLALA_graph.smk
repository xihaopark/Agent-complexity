configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "download_HLALA_graph"


rule all:
  input:
    "results/finish/download_HLALA_graph.done"


rule run_download_HLALA_graph:
  output:
    "results/finish/download_HLALA_graph.done"
  run:
    run_step(STEP_ID, output[0])
