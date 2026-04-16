configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "vcf_to_bcf"


rule all:
  input:
    "results/finish/vcf_to_bcf.done"


rule run_vcf_to_bcf:
  output:
    "results/finish/vcf_to_bcf.done"
  run:
    run_step(STEP_ID, output[0])
