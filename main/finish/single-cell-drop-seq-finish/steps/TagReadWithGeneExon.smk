configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "TagReadWithGeneExon"


rule all:
  input:
    "results/finish/TagReadWithGeneExon.done"


rule run_TagReadWithGeneExon:
  output:
    "results/finish/TagReadWithGeneExon.done"
  run:
    run_step(STEP_ID, output[0])
