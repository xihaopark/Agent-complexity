configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "call_all_differential_srna_clusters"


rule all:
  input:
    "results/finish/call_all_differential_srna_clusters.done"


rule run_call_all_differential_srna_clusters:
  output:
    "results/finish/call_all_differential_srna_clusters.done"
  run:
    run_step(STEP_ID, output[0])
