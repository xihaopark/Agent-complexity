configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "annotation_ChIPpeakAnno"


rule all:
  input:
    "results/finish/annotation_ChIPpeakAnno.done"


rule run_annotation_ChIPpeakAnno:
  output:
    "results/finish/annotation_ChIPpeakAnno.done"
  run:
    run_step(STEP_ID, output[0])
