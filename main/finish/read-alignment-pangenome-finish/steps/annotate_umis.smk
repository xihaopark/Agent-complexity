configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "annotate_umis"


rule all:
  input:
    "results/finish/annotate_umis.done"


rule run_annotate_umis:
  output:
    "results/finish/annotate_umis.done"
  run:
    run_step(STEP_ID, output[0])
