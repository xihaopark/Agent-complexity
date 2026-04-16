configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "annotate_unique_fp_fn"


rule all:
  input:
    "results/finish/annotate_unique_fp_fn.done"


rule run_annotate_unique_fp_fn:
  output:
    "results/finish/annotate_unique_fp_fn.done"
  run:
    run_step(STEP_ID, output[0])
