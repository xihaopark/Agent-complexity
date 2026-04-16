configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "write_shared_fn_vcf"


rule all:
  input:
    "results/finish/write_shared_fn_vcf.done"


rule run_write_shared_fn_vcf:
  output:
    "results/finish/write_shared_fn_vcf.done"
  run:
    run_step(STEP_ID, output[0])
