configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "write_unique_fp_vcf"


rule all:
  input:
    "results/finish/write_unique_fp_vcf.done"


rule run_write_unique_fp_vcf:
  output:
    "results/finish/write_unique_fp_vcf.done"
  run:
    run_step(STEP_ID, output[0])
