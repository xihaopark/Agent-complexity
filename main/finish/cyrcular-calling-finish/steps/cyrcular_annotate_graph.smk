configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "cyrcular_annotate_graph"


rule all:
  input:
    "results/finish/cyrcular_annotate_graph.done"


rule run_cyrcular_annotate_graph:
  output:
    "results/finish/cyrcular_annotate_graph.done"
  run:
    run_step(STEP_ID, output[0])
