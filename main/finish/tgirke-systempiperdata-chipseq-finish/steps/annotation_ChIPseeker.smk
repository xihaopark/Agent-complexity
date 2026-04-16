configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "annotation_ChIPseeker"


rule all:
  input:
    "results/finish/annotation_ChIPseeker.done"


rule run_annotation_ChIPseeker:
  output:
    "results/finish/annotation_ChIPseeker.done"
  run:
    run_step(STEP_ID, output[0])
