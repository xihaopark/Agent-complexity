configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "annotate_shared_fn"


rule all:
  input:
    "results/finish/annotate_shared_fn.done"


rule run_annotate_shared_fn:
  output:
    "results/finish/annotate_shared_fn.done"
  run:
    run_step(STEP_ID, output[0])
