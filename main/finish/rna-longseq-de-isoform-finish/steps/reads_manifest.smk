configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "reads_manifest"


rule all:
  input:
    "results/finish/reads_manifest.done"


rule run_reads_manifest:
  output:
    "results/finish/reads_manifest.done"
  run:
    run_step(STEP_ID, output[0])
