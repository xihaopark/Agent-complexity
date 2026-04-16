configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "consensus_peaks"


rule all:
  input:
    "results/finish/consensus_peaks.done"


rule run_consensus_peaks:
  output:
    "results/finish/consensus_peaks.done"
  run:
    run_step(STEP_ID, output[0])
