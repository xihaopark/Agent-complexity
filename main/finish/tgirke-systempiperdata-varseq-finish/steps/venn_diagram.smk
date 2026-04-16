configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "venn_diagram"


rule all:
  input:
    "results/finish/venn_diagram.done"


rule run_venn_diagram:
  output:
    "results/finish/venn_diagram.done"
  run:
    run_step(STEP_ID, output[0])
