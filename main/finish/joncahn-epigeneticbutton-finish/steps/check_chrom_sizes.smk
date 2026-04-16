configfile: "config_basic/config.yaml"

include: "common.smk"

STEP_ID = "check_chrom_sizes"


rule all:
  input:
    "results/finish/check_chrom_sizes.done"


rule run_check_chrom_sizes:
  output:
    "results/finish/check_chrom_sizes.done"
  run:
    run_step(STEP_ID, output[0])
