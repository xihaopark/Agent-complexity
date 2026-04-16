configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "restrict_to_reference_contigs"


rule all:
  input:
    "results/finish/restrict_to_reference_contigs.done"


rule run_restrict_to_reference_contigs:
  output:
    "results/finish/restrict_to_reference_contigs.done"
  run:
    run_step(STEP_ID, output[0])
