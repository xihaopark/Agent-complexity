configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "phantompeak_multiqc"


rule all:
  input:
    "results/finish/phantompeak_multiqc.done"


rule run_phantompeak_multiqc:
  output:
    "results/finish/phantompeak_multiqc.done"
  run:
    run_step(STEP_ID, output[0])
