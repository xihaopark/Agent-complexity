configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "annotate_strelka_variants"


rule all:
  input:
    "results/finish/annotate_strelka_variants.done"


rule run_annotate_strelka_variants:
  output:
    "results/finish/annotate_strelka_variants.done"
  run:
    run_step(STEP_ID, output[0])
