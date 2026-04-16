configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "ont_3a_readQC_downsample"


rule all:
  input:
    "results/finish/ont_3a_readQC_downsample.done"


rule run_ont_3a_readQC_downsample:
  output:
    "results/finish/ont_3a_readQC_downsample.done"
  run:
    run_step(STEP_ID, output[0])
