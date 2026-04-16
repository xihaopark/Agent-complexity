#!/usr/bin/env bash

module purge;

module load slurm/19.05.8;
module load GCC;
module load bzip2;
module load GSL;
module load zlib;
module load OpenSSL;
module load PCRE;
module load XZ;
module load libdeflate;

module load Boost/1.67.0-foss-2018b;
module load Java/1.8.0_292-OpenJDK;

module load HTSlib/1.10.2-GCC-9.3.0;
module load SAMtools/1.9-foss-2018b
module load BCFtools/1.10.2-GCC-9.3.0;
module load BWA/0.7.17-GCC-9.3.0;
module load BEDTools/2.29.2-GCC-9.3.0;
module load Perl/5.28.0-GCCcore-7.3.0;
module load Bowtie2/2.3.4.2-foss-2018b
module load fftw3/openmpi/gcc/64/3.3.8;
module load R/3.5.1-foss-2018b; 
module load FastQC/0.11.8-Java-1.8;
module load Bismark/0.20.1-foss-2018b;
module load Sambamba/0.6.6;

module load picard/2.18.27-Java-1.8;

# from ucsc-tools you need the bedSort and bedToBigBed (v2.8) in your PATH
# you need skewer (v0.2.2) in your PATH

export PEPENV=$(pwd)/pipeline/env_config/pepenv/cemm.yaml

# Activate python environment for atacseq pipeline
conda activate bcg_pipeline;

module unload Python;
