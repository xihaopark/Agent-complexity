configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "annotate_variants"


rule all:
  input:
    "results/finish/annotate_variants.done"


rule run_annotate_variants:
  output:
    "results/finish/annotate_variants.done"
  run:
    run_step(STEP_ID, output[0])
