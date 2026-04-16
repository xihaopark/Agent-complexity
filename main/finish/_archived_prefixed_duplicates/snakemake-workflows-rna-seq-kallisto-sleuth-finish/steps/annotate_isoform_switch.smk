configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "annotate_isoform_switch"


rule all:
  input:
    "results/finish/annotate_isoform_switch.done"


rule run_annotate_isoform_switch:
  output:
    "results/finish/annotate_isoform_switch.done"
  run:
    run_step(STEP_ID, output[0])
