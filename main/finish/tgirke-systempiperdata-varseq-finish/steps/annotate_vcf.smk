configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "annotate_vcf"


rule all:
  input:
    "results/finish/annotate_vcf.done"


rule run_annotate_vcf:
  output:
    "results/finish/annotate_vcf.done"
  run:
    run_step(STEP_ID, output[0])
