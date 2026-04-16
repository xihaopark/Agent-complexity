configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "deduplicate_srna_nextflexv3"


rule all:
  input:
    "results/finish/deduplicate_srna_nextflexv3.done"


rule run_deduplicate_srna_nextflexv3:
  output:
    "results/finish/deduplicate_srna_nextflexv3.done"
  run:
    run_step(STEP_ID, output[0])
