configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "homer_consensus_annotatepeaks"


rule all:
  input:
    "results/finish/homer_consensus_annotatepeaks.done"


rule run_homer_consensus_annotatepeaks:
  output:
    "results/finish/homer_consensus_annotatepeaks.done"
  run:
    run_step(STEP_ID, output[0])
