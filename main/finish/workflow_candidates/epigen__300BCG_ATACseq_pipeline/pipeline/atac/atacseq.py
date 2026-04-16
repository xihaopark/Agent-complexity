#!/usr/bin/env python

"""
ATAC-seq pipeline
"""

import os
import sys
import yaml
import StringIO
import zipfile
import re
from subprocess import check_output
from collections import defaultdict
from argparse import ArgumentParser

import pandas as pd
import pybedtools

import pypiper
from pypiper.ngstk import NGSTk
from peppy import AttributeDict, Sample

__author__ = "Andre Rendeiro"
__copyright__ = "Copyright 2015, Andre Rendeiro"
__credits__ = []
__license__ = "GPL2"
__version__ = "0.2"
__maintainer__ = "Andre Rendeiro"
__email__ = "arendeiro@cemm.oeaw.ac.at"
__status__ = "Development"


class ATACseqSample(Sample):
    """
    Class to model ATAC-seq samples based on the ChIPseqSample class.

    :param series: Pandas `Series` object.
    :type series: pandas.Series
    """
    __library__ = "ATAC-seq"

    def __init__(self, series):

        # Use pd.Series object to have all sample attributes
        if not isinstance(series, pd.Series):
            raise TypeError("Provided object is not a pandas Series.")
        super(ATACseqSample, self).__init__(series)

    def __repr__(self):
        return "ATAC-seq sample '%s'" % self.sample_name

    def set_file_paths(self):
        """
        Sets the paths of all files for this sample.
        """
        # Inherit paths from Sample by running Sample's set_file_paths()
        super(ATACseqSample, self).set_file_paths()

        # Files in the root of the sample dir
        self.fastqc = os.path.join(self.paths.sample_root, self.sample_name + ".fastqc.zip")
        self.trimlog = os.path.join(self.paths.sample_root, self.sample_name + ".trimlog.txt")
        self.aln_rates = os.path.join(self.paths.sample_root, self.sample_name + ".aln_rates.txt")
        self.aln_metrics = os.path.join(self.paths.sample_root, self.sample_name + ".aln_metrics.txt")
        self.dups_metrics = os.path.join(self.paths.sample_root, self.sample_name + ".dups_metrics.txt")
        self.dups_filtered_metrics = os.path.join(self.paths.sample_root, self.sample_name + ".dups_filtered_metrics.txt")
        self.mitochondrial_metrics = os.path.join(self.paths.sample_root, self.name + ".mito_metrics.txt")
        
        # Unmapped: merged bam, fastq, trimmed fastq
        self.paths.unmapped = os.path.join(self.paths.sample_root, "unmapped")
        self.unmapped = os.path.join(self.paths.unmapped, self.sample_name + ".bam")
        self.fastq = os.path.join(self.paths.unmapped, self.sample_name + ".fastq")
        self.fastq1 = os.path.join(self.paths.unmapped, self.sample_name + ".1.fastq")
        self.fastq2 = os.path.join(self.paths.unmapped, self.sample_name + ".2.fastq")
        self.fastq_unpaired = os.path.join(self.paths.unmapped, self.sample_name + ".unpaired.fastq")
        self.trimmed = os.path.join(self.paths.unmapped, self.sample_name + ".trimmed.fastq")
        self.trimmed1 = os.path.join(self.paths.unmapped, self.sample_name + ".1.trimmed.fastq")
        self.trimmed2 = os.path.join(self.paths.unmapped, self.sample_name + ".2.trimmed.fastq")
        self.trimmed1_unpaired = os.path.join(self.paths.unmapped, self.sample_name + ".1_unpaired.trimmed.fastq")
        self.trimmed2_unpaired = os.path.join(self.paths.unmapped, self.sample_name + ".2_unpaired.trimmed.fastq")

        # Mapped: mapped, duplicates marked, removed, reads shifted
        self.paths.mapped = os.path.join(self.paths.sample_root, "mapped")
        self.mapped = os.path.join(self.paths.mapped, self.sample_name + ".trimmed.bowtie2.bam")
        self.markdup = os.path.join(self.paths.mapped, self.sample_name + ".trimmed.bowtie2.markdup.bam")
        self.filtered = os.path.join(self.paths.mapped, self.sample_name + ".trimmed.bowtie2.filtered.bam")

        # Transposition events
        self.transposition_events = os.path.join(self.paths.mapped,
                                                 "{}.trimmed.bowtie2.filtered.shifted.events.bed".format(self.name))

        # Coverage: read coverage in windows genome-wide
        self.paths.coverage = os.path.join(self.paths.sample_root, "coverage")
        self.coverage = os.path.join(self.paths.coverage, self.name + ".cov")

        self.bigwig = os.path.join(self.paths.coverage, self.name + ".bigWig")

        self.insertplot = os.path.join(self.paths.sample_root, self.name + "_insertLengths.pdf")
        self.insertdata = os.path.join(self.paths.sample_root, self.name + "_insertLengths.csv")
        
        self.qc = os.path.join(self.paths.sample_root, self.name + "_qc.tsv")
        self.qc_plot = os.path.join(self.paths.sample_root, self.name + "_qc.pdf")

        # Peaks: peaks called and derivate files
        self.paths.peaks = os.path.join(self.paths.sample_root, "peaks")
        self.peaks = os.path.join(self.paths.peaks, self.name + "_peaks.narrowPeak")
        self.sortedpeaks = os.path.join(self.paths.peaks, self.name + "_peaks.sorted.narrowPeak")

        self.summits = os.path.join(self.paths.peaks, self.name + "_summits.bed")
        self.filtered_peaks = os.path.join(self.paths.peaks, self.name + "_peaks.filtered.bed")

        #Quantification
        self.peaks_quantification=os.path.join(self.paths.sample_root, "{}_peaks.quantification.bed".format(self.name))
        self.oracle_quantification = os.path.join(self.paths.sample_root, "{}_oracle.quantification.bed".format(self.name))

        #TSS data
        self.tss_table = os.path.join(self.paths.sample_root, "{}_TSS.csv".format(self.name))
        self.tss_plot = os.path.join(self.paths.sample_root, "{}_TSS.svg".format(self.name))
        self.tss_completed = os.path.join(self.paths.sample_root, "{}_TSS.complete".format(self.name))

def main():
    # Parse command-line arguments
    parser = ArgumentParser(
        prog="atacseq-pipeline",
        description="ATAC-seq pipeline."
    )
    parser = arg_parser(parser)
    parser = pypiper.add_pypiper_args(parser, groups=["ngs", "looper", "resource", "pypiper"])
    args = parser.parse_args()

    # Read in yaml configs
    series = pd.Series(yaml.load(open(args.sample_config, "r")))

    # looper 0.6/0.7 compatibility:
    if "protocol" in series.index:
        key = "protocol"
    elif "library" in series.index:
        key = "library"
    else:
        raise KeyError(
            "Sample does not contain either a 'protocol' or 'library' attribute!")

    # Create Sample object
    if series[key] != "DNase-seq":
        sample = ATACseqSample(series)
    else:
         raise Exception(
            "DNase-seq samples not supported"
         )

    # Check if merged
    if len(sample.data_path.split(" ")) > 1:
        sample.merged = True
    else:
        sample.merged = False
    sample.prj = AttributeDict(sample.prj)
    sample.paths = AttributeDict(sample.paths.__dict__)

    # Check read type if not provided
    if not hasattr(sample, "ngs_inputs"):
        sample.ngs_inputs = [sample.data_source]
    if not hasattr(sample, "read_type"):
        sample.set_read_type()
    else:
        if sample.read_type not in ['single', 'paired']:
            sample.set_read_type()

    # Shorthand for read_type
    if sample.read_type == "paired":
        sample.paired = True
    else:
        sample.paired = False

    # Set file paths
    sample.set_file_paths()
    # sample.make_sample_dirs()  # should be fixed to check if values of paths are strings and paths indeed

    # Start Pypiper object
    # Best practice is to name the pipeline with the name of the script;
    # or put the name in the pipeline interface.
    pipe_manager = pypiper.PipelineManager(name="atacseq", outfolder=sample.paths.sample_root, args=args)
    pipe_manager.config.tools.scripts_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "tools")

    # Start main function
    process(sample, pipe_manager, args)


def arg_parser(parser):
    """
    Global options for pipeline.
    """
    parser.add_argument(
        "-y", "--sample-yaml",
        dest="sample_config",
        help="Yaml config file with sample attributes.",
        type=str)
    return parser


def process(sample, pipe_manager, args):
    """
    This takes unmapped Bam files and makes trimmed, aligned, duplicate marked
    and removed, indexed, shifted Bam files along with a UCSC browser track.
    Peaks are called and filtered.
    """
    print("Start processing ATAC-seq sample %s." % sample.sample_name)

    for path in ["sample_root"] + list(sample.paths.__dict__.keys()):
        try:
            exists = os.path.exists(sample.paths[path])
        except TypeError:
            continue
        if not exists:
            try:
                os.mkdir(sample.paths[path])
            except OSError("Cannot create '%s' path: %s" % (path, sample.paths[path])):
                raise

    # Create NGSTk instance
    tk = NGSTk(pm=pipe_manager)

    # Merge Bam files if more than one technical replicate
    if len(sample.data_path.split(" ")) > 1:
        pipe_manager.timestamp("Merging bam files from replicates")
        cmd = tk.merge_bams(
            input_bams=sample.data_path.split(" "),  # this is a list of sample paths
            merged_bam=sample.unmapped
        )
        pipe_manager.run(cmd, sample.unmapped, shell=True)
        sample.data_path = sample.unmapped

    # Fastqc
    pipe_manager.timestamp("Measuring sample quality with Fastqc")
    cmd = tk.fastqc_rename(
        input_bam=sample.data_path,
        output_dir=sample.paths.sample_root,
        sample_name=sample.sample_name
    )
    pipe_manager.run(cmd, os.path.join(sample.paths.sample_root, sample.sample_name + "_fastqc.zip"), shell=True)
    report_dict(pipe_manager, parse_fastqc(os.path.join(sample.paths.sample_root, sample.sample_name + "_fastqc.zip"), prefix="fastqc_"))

    # Convert bam to fastq
    pipe_manager.timestamp("Converting to Fastq format")
    cmd = tk.bam2fastq(
        inputBam=sample.data_path,
        outputFastq=sample.fastq1 if sample.paired else sample.fastq,
        outputFastq2=sample.fastq2 if sample.paired else None,
        unpairedFastq=sample.fastq_unpaired if sample.paired else None
    )
    pipe_manager.run(cmd, sample.fastq1 if sample.paired else sample.fastq, shell=True)
    if not sample.paired:
        pipe_manager.clean_add(sample.fastq, conditional=True)
    if sample.paired:
        pipe_manager.clean_add(sample.fastq1, conditional=True)
        pipe_manager.clean_add(sample.fastq2, conditional=True)
        pipe_manager.clean_add(sample.fastq_unpaired, conditional=True)

    # Trim reads
    pipe_manager.timestamp("Trimming adapters from sample")
    if pipe_manager.config.parameters.trimmer == "trimmomatic":
        cmd = tk.trimmomatic(
            inputFastq1=sample.fastq1 if sample.paired else sample.fastq,
            inputFastq2=sample.fastq2 if sample.paired else None,
            outputFastq1=sample.trimmed1 if sample.paired else sample.trimmed,
            outputFastq1unpaired=sample.trimmed1_unpaired if sample.paired else None,
            outputFastq2=sample.trimmed2 if sample.paired else None,
            outputFastq2unpaired=sample.trimmed2_unpaired if sample.paired else None,
            cpus=args.cores,
            adapters=pipe_manager.config.resources.adapters,
            log=sample.trimlog
        )
        pipe_manager.run(cmd, sample.trimmed1 if sample.paired else sample.trimmed, shell=True)
        if not sample.paired:
            pipe_manager.clean_add(sample.trimmed, conditional=True)
        else:
            pipe_manager.clean_add(sample.trimmed1, conditional=True)
            pipe_manager.clean_add(sample.trimmed1_unpaired, conditional=True)
            pipe_manager.clean_add(sample.trimmed2, conditional=True)
            pipe_manager.clean_add(sample.trimmed2_unpaired, conditional=True)

    elif pipe_manager.config.parameters.trimmer == "skewer":
        cmd = tk.skewer(
            inputFastq1=sample.fastq1 if sample.paired else sample.fastq,
            inputFastq2=sample.fastq2 if sample.paired else None,
            outputPrefix=os.path.join(sample.paths.unmapped, sample.sample_name),
            outputFastq1=sample.trimmed1 if sample.paired else sample.trimmed,
            outputFastq2=sample.trimmed2 if sample.paired else None,
            trimLog=sample.trimlog,
            cpus=args.cores,
            adapters=pipe_manager.config.resources.adapters
        )
        pipe_manager.run(cmd, sample.trimmed1 if sample.paired else sample.trimmed, shell=True)
        if not sample.paired:
            pipe_manager.clean_add(sample.trimmed, conditional=True)
        else:
            pipe_manager.clean_add(sample.trimmed1, conditional=True)
            pipe_manager.clean_add(sample.trimmed2, conditional=True)

        report_dict(pipe_manager, parse_trim_stats(sample.trimlog, prefix="trim_", paired_end=sample.paired))

    # Map
    pipe_manager.timestamp("Mapping reads with Bowtie2")
    cmd = tk.bowtie2Map(
        inputFastq1=sample.trimmed1 if sample.paired else sample.trimmed,
        inputFastq2=sample.trimmed2 if sample.paired else None,
        outputBam=sample.mapped,
        log=sample.aln_rates,
        metrics=sample.aln_metrics,
        genomeIndex=getattr(pipe_manager.config.resources.genome_index, sample.genome),
        maxInsert=pipe_manager.config.parameters.max_insert,
        cpus=args.cores
    )
    pipe_manager.run(cmd, sample.mapped, shell=True)
    report_dict(pipe_manager, parse_mapping_stats(sample.aln_rates, paired_end=sample.paired))
    
    # Index and Markdup
    pipe_manager.timestamp("Marking duplicates")
    cmd = index_markdup_bam_file(
        tk,
        cpus=args.cores,
        input_bam_file=sample.mapped,
        output_bam_file=sample.markdup,
        duplicate_stats=sample.dups_metrics
    )
    pipe_manager.run(cmd, sample.dups_metrics, shell=True)
    report_dict(pipe_manager, parse_flagstats(sample.dups_metrics))

    # Get mitochondrial reads get_mitochondrial_stats(tk, bam_file, output, cpus=4, mt_chrom="chrM"):
    pipe_manager.timestamp("Getting mitochondrial stats")
    cmd = get_mitochondrial_stats(
        tk,
        bam_file=sample.markdup,
        output=sample.mitochondrial_metrics,
        cpus=args.cores
    )
    pipe_manager.run(cmd, sample.mitochondrial_metrics, shell=True, nofail=True)
    report_dict(pipe_manager, parse_flagstats(sample.mitochondrial_metrics, prefix="MT_"))

    # Filter reads
    pipe_manager.timestamp("Filtering reads for quality")
    cmd = filter_reads(
        tk,               
        input_bam=sample.markdup,
        output_bam=sample.filtered,
        metrics_file=sample.dups_filtered_metrics,
        paired=sample.paired,
        cpus=args.cores,
        Q=pipe_manager.config.parameters.read_quality
    )
    pipe_manager.run(cmd, sample.dups_filtered_metrics, shell=True)
    report_dict(pipe_manager, parse_flagstats(sample.dups_filtered_metrics,prefix="filtered_"))

    # Report total efficiency
    usable = float(pipe_manager.stats_dict["filtered_mapped_reads"])
    total = float(pipe_manager.stats_dict['fastqc_total_pass_filter_reads'])
    report_dict(
        pipe_manager,
        {"total_efficiency": (usable / total) * 100})

    # Extract transposition events, accounting for transposase bias
    cmd=calculate_transposition_events(
        sample.filtered,
        sample.transposition_events,
        pipe_manager.config.resources.chromosome_sizes[sample.genome]
    )
    pipe_manager.run(cmd, sample.transposition_events, shell=True)

    # Call peaks
    pipe_manager.timestamp("Calling peaks with MACS2")
    # make dir for output (macs fails if it does not exist)
    if not os.path.exists(sample.paths.peaks):
        os.makedirs(sample.paths.peaks)

    cmd = tk.macs2CallPeaksATACSeq(
        treatmentBam=sample.filtered,
        outputDir=sample.paths.peaks,
        sampleName=sample.sample_name,
        genome=sample.genome
    )
    pipe_manager.run(cmd, sample.peaks, shell=True)
    pipe_manager.clean_add(sample.peaks)

    # Sort peaks
    cmd = "bedtools sort -faidx {} -i {} > {}".format(
        pipe_manager.config.resources.chromosome_sizes[sample.genome],
        sample.peaks,
        sample.sortedpeaks
    )
    pipe_manager.run(cmd, sample.sortedpeaks, shell=True)
    report_dict(pipe_manager, parse_peak_number(sample.sortedpeaks))

    # Filter peaks
    if hasattr(pipe_manager.config.resources.blacklisted_regions, sample.genome):
        pipe_manager.timestamp("Filtering peaks from blacklisted regions")
        cmd = filter_peaks(
            peaks=sample.sortedpeaks,
            exclude=getattr(pipe_manager.config.resources.blacklisted_regions, sample.genome),
            filtered_peaks=sample.filtered_peaks
        )
        pipe_manager.run(cmd, sample.filtered_peaks, shell=True)
        report_dict(pipe_manager, parse_peak_number(sample.filtered_peaks, prefix="filtered_"))

    # Quantify events in peaks
    pipe_manager.timestamp("Calculating events in peaks (FRiP)")
    cmd = quantify(
        sample.transposition_events,
        sample.sortedpeaks,
        sample.peaks_quantification,
        pipe_manager.config.resources.chromosome_sizes[sample.genome]
    )
    pipe_manager.run(cmd, sample.peaks_quantification, shell=True)
    report_dict(pipe_manager, parse_FRiP(sample.peaks_quantification, usable))


    if hasattr(pipe_manager.config.resources.oracle_peak_regions, sample.genome):
        # Quantify events in oracle regions
        pipe_manager.timestamp("Calculating events in oracle regions (oracle_FRiP)")
        cmd = quantify(
            sample.transposition_events,
            pipe_manager.config.resources.oracle_peak_regions[sample.genome],
            sample.oracle_quantification,
            pipe_manager.config.resources.chromosome_sizes[sample.genome]
        )
        pipe_manager.run(cmd, sample.oracle_quantification, shell=True)
        report_dict(pipe_manager, parse_FRiP(sample.oracle_quantification, usable,prefix="oracle_"))

    # Plot fragment distribution
    if sample.paired and not os.path.exists(sample.insertplot):
        pipe_manager.timestamp("Plotting insert size distribution")
        tk.plot_atacseq_insert_sizes(
            bam=sample.filtered,
            plot=sample.insertplot,
            output_csv=sample.insertdata
        )
        pipe_manager.report_figure("insert_sizes", sample.insertplot)

    # Count coverage genome-wide
    # pipe_manager.timestamp("Calculating genome-wide coverage")
    # cmd = tk.genomeWideCoverage(
    #     inputBam=sample.filtered,
    #     genomeWindows=getattr(pipe_manager.config.resources.genome_windows, sample.genome),
    #     output=sample.coverage
    # )
    # pipe_manager.run(cmd, sample.coverage, shell=True)

    # Calculate NSC, RSC
#     pipe_manager.timestamp("Assessing signal/noise in sample")
#     cmd = tk.peakTools(
#         inputBam=sample.filtered,
#         output=sample.qc,
#         plot=sample.qc_plot,
#         cpus=args.cores
#     )
#     pipe_manager.run(cmd, sample.qc_plot, shell=True, nofail=True)
#     report_dict(pipe_manager, parse_nsc_rsc(sample.qc))
#     pipe_manager.report_figure("cross_correlation", sample.qc_plot)

    # Calculate TSS enrichment
    if hasattr(pipe_manager.config.resources.tss_regions, sample.genome):
        pipe_manager.timestamp("Calculating TSS enrichment in sample")
        cmd = calculate_tss(
            sample.transposition_events,
            pipe_manager.config.resources.chromosome_sizes[sample.genome],
            sample.name,
            pipe_manager.config.resources.tss_regions[sample.genome],
            sample.paths.sample_root
        )
        pipe_manager.run(cmd, sample.tss_completed, shell=True)
        tss_enrich = float(pd.read_csv(sample.tss_table,index_col='base').max())
        report_dict(pipe_manager, {'tss_enrichment':tss_enrich})
        pipe_manager.report_figure("tss_enrichment", sample.tss_plot)
    
    # Make tracks
    track_dir = os.path.dirname(sample.bigwig)
    if not os.path.exists(track_dir):
        os.makedirs(track_dir)
    # right now tracks are only made for bams without duplicates
    pipe_manager.timestamp("Making bigWig tracks from BAM file")
    cmd = bam_to_bigwig(
        input_bam=sample.filtered,
        output_bigwig=sample.bigwig,
        genome=sample.genome,
        normalization_method="RPGC")
    pipe_manager.run(cmd, sample.bigwig, shell=True)

    # Finish up
    print(pipe_manager.stats_dict)

    pipe_manager.stop_pipeline()
    print("Finished processing sample %s." % sample.sample_name)


def report_dict(pipe, stats_dict):
    for key, value in stats_dict.items():
        pipe.report_result(key, value)


def parse_fastqc(fastqc_zip, prefix=""):
    """
    """

    error_dict = {
        prefix + "total_pass_filter_reads": pd.np.nan,
        prefix + "poor_quality": pd.np.nan,
        prefix + "read_length": pd.np.nan,
        prefix + "GC_perc": pd.np.nan}

    try:
        zfile = zipfile.ZipFile(fastqc_zip)
        content = StringIO.StringIO(zfile.read(os.path.join(zfile.filelist[0].filename, "fastqc_data.txt"))).readlines()
    except:
        return error_dict
    try:
        line = [i for i in range(len(content)) if "Total Sequences" in content[i]][0]
        total = int(re.sub(r"\D", "", re.sub(r"\(.*", "", content[line])))
        line = [i for i in range(len(content)) if "Sequences flagged as poor quality" in content[i]][0]
        poor_quality = int(re.sub(r"\D", "", re.sub(r"\(.*", "", content[line])))
        line = [i for i in range(len(content)) if "Sequence length" in content[i]][0]
        seq_len = int(re.sub(r"\D", "", re.sub(r" \(.*", "", content[line]).strip()))
        line = [i for i in range(len(content)) if "%GC" in content[i]][0]
        gc_perc = int(re.sub(r"\D", "", re.sub(r" \(.*", "", content[line]).strip()))
        return {
            prefix + "total_pass_filter_reads": total,
            prefix + "poor_quality_perc": (float(poor_quality) / total) * 100,
            prefix + "read_length": seq_len,
            prefix + "GC_perc": gc_perc}
    except IndexError:
        return error_dict


def parse_trim_stats(stats_file, prefix="", paired_end=True):
    """
    :param stats_file: sambamba output file with duplicate statistics.
    :type stats_file: str
    :param prefix: A string to be used as prefix to the output dictionary keys.
    :type stats_file: str
    """

    stats_dict = {
        prefix + "surviving_perc": pd.np.nan,
        prefix + "short_perc": pd.np.nan,
        prefix + "empty_perc": pd.np.nan,
        prefix + "trimmed_perc": pd.np.nan,
        prefix + "untrimmed_perc": pd.np.nan,
        prefix + "trim_loss_perc": pd.np.nan}
    try:
        with open(stats_file) as handle:
            content = handle.readlines()  # list of strings per line
    except:
        return stats_dict

    suf = "s" if not paired_end else " pairs"

    try:
        line = [i for i in range(len(content)) if "read{} processed; of these:".format(suf) in content[i]][0]
        total = int(re.sub(r"\D", "", re.sub(r"\(.*", "", content[line])))
    except IndexError:
        return stats_dict
    try:
        line = [i for i in range(len(content)) if "read{} available; of these:".format(suf) in content[i]][0]
        surviving = int(re.sub(r"\D", "", re.sub(r"\(.*", "", content[line])))
        stats_dict[prefix + "surviving_perc"] = (float(surviving) / total) * 100
        stats_dict[prefix + "trim_loss_perc"] = ((total - float(surviving)) / total) * 100
    except IndexError:
        pass
    try:
        line = [i for i in range(len(content)) if "short read{} filtered out after trimming by size control".format(suf) in content[i]][0]
        short = int(re.sub(r" \(.*", "", content[line]).strip())
        stats_dict[prefix + "short_perc"] = (float(short) / total) * 100
    except IndexError:
        pass
    try:
        line = [i for i in range(len(content)) if "empty read{} filtered out after trimming by size control".format(suf) in content[i]][0]
        empty = int(re.sub(r" \(.*", "", content[line]).strip())
        stats_dict[prefix + "empty_perc"] = (float(empty) / total) * 100
    except IndexError:
        pass
    try:
        line = [i for i in range(len(content)) if "trimmed read{} available after processing".format(suf) in content[i]][0]
        trimmed = int(re.sub(r" \(.*", "", content[line]).strip())
        stats_dict[prefix + "trimmed_perc"] = (float(trimmed) / total) * 100
    except IndexError:
        pass
    try:
        line = [i for i in range(len(content)) if "untrimmed read{} available after processing".format(suf) in content[i]][0]
        untrimmed = int(re.sub(r" \(.*", "", content[line]).strip())
        stats_dict[prefix + "untrimmed_perc"] = (float(untrimmed) / total) * 100
    except IndexError:
        pass
    return stats_dict


def parse_mapping_stats(stats_file, prefix="", paired_end=True):
    """
    :param stats_file: sambamba output file with duplicate statistics.
    :type stats_file: str
    :param prefix: A string to be used as prefix to the output dictionary keys.
    :type stats_file: str
    """

    if not paired_end:
        error_dict = {
            prefix + "not_aligned_perc": pd.np.nan,
            prefix + "unique_aligned_perc": pd.np.nan,
            prefix + "multiple_aligned_perc": pd.np.nan,
            prefix + "perc_aligned": pd.np.nan}
    else:
        error_dict = {
            prefix + "paired_perc": pd.np.nan,
            prefix + "concordant_perc": pd.np.nan,
            prefix + "concordant_unique_perc": pd.np.nan,
            prefix + "concordant_multiple_perc": pd.np.nan,
            prefix + "not_aligned_or_discordant_perc": pd.np.nan,
            prefix + "not_aligned_perc": pd.np.nan,
            prefix + "unique_aligned_perc": pd.np.nan,
            prefix + "multiple_aligned_perc": pd.np.nan,
            prefix + "perc_aligned": pd.np.nan}

    try:
        with open(stats_file) as handle:
            content = handle.readlines()  # list of strings per line
    except:
        return error_dict

    if not paired_end:
        try:
            line = [i for i in range(len(content)) if "reads; of these:" in content[i]][0]
            total = int(re.sub(r"\D", "", re.sub(r"\(.*", "", content[line])))
            line = [i for i in range(len(content)) if "aligned 0 times" in content[i]][0]
            not_aligned_perc = float(re.search(r"\(.*%\)", content[line]).group()[1:-2])
            line = [i for i in range(len(content)) if " aligned exactly 1 time" in content[i]][0]
            unique_aligned_perc = float(re.search(r"\(.*%\)", content[line]).group()[1:-2])
            line = [i for i in range(len(content)) if " aligned >1 times" in content[i]][0]
            multiple_aligned_perc = float(re.search(r"\(.*%\)", content[line]).group()[1:-2])
            line = [i for i in range(len(content)) if "overall alignment rate" in content[i]][0]
            perc_aligned = float(re.sub("%.*", "", content[line]).strip())
            return {
                prefix + "not_aligned_perc": not_aligned_perc,
                prefix + "unique_aligned_perc": unique_aligned_perc,
                prefix + "multiple_aligned_perc": multiple_aligned_perc,
                prefix + "perc_aligned": perc_aligned}
        except IndexError:
            return error_dict

    if paired_end:
        try:
            line = [i for i in range(len(content)) if "reads; of these:" in content[i]][0]
            total = int(re.sub(r"\D", "", re.sub(r"\(.*", "", content[line]))) #THOSE ARE READ PAIRS
            line = [i for i in range(len(content)) if " were paired; of these:" in content[i]][0]
            paired_perc = float(re.search(r"\(.*%\)", content[line]).group()[1:-2])
            line = [i for i in range(len(content)) if "aligned concordantly 0 times" in content[i]][0]
            concordant_unaligned_perc = float(re.search(r"\(.*%\)", content[line]).group()[1:-2])
            line = [i for i in range(len(content)) if "aligned concordantly exactly 1 time" in content[i]][0]
            concordant_unique_perc = float(re.search(r"\(.*%\)", content[line]).group()[1:-2])
            line = [i for i in range(len(content)) if "aligned concordantly >1 times" in content[i]][0]
            concordant_multiple_perc = float(re.search(r"\(.*%\)", content[line]).group()[1:-2])
            
            line = [i for i in range(len(content)) if "mates make up the pairs; of these:" in content[i]][0]
            not_aligned_or_discordant = int(re.sub(r"\D", "", re.sub(r"\(.*", "", content[line]))) #THOSE ARE PAIR MATES
            d_fraction = (not_aligned_or_discordant / float(total*2))
            not_aligned_or_discordant_perc = d_fraction * 100
            
            line = [i for i in range(len(content)) if "aligned 0 times\n" in content[i]][0]
            not_aligned_perc = float(re.search(r"\(.*%\)", content[line]).group()[1:-2]) * d_fraction
            
            line = [i for i in range(len(content)) if " aligned exactly 1 time" in content[i]][0]
            unique_aligned_perc = float(re.search(r"\(.*%\)", content[line]).group()[1:-2]) * d_fraction
            
            line = [i for i in range(len(content)) if " aligned >1 times" in content[i]][0]
            multiple_aligned_perc = float(re.search(r"\(.*%\)", content[line]).group()[1:-2]) * d_fraction
            
            line = [i for i in range(len(content)) if "overall alignment rate" in content[i]][0]
            perc_aligned = float(re.sub("%.*", "", content[line]).strip())
            
            return {
                prefix + "paired_perc": paired_perc,
                prefix + "concordant_unaligned_perc": concordant_unaligned_perc,
                prefix + "concordant_unique_perc": concordant_unique_perc,
                prefix + "concordant_multiple_perc": concordant_multiple_perc,
                prefix + "not_aligned_or_discordant_perc": not_aligned_or_discordant_perc,
                prefix + "not_aligned_perc": not_aligned_perc,
                prefix + "discordant_unique_aligned_perc": unique_aligned_perc,
                prefix + "discordant_multiple_aligned_perc": multiple_aligned_perc,
                prefix + "perc_aligned": perc_aligned}
        except IndexError:
            return error_dict

def parse_flagstats(stats_file, prefix=""):

    error_dict = {
        prefix + "mapped_reads": pd.np.nan,
        prefix + "duplicate_percentage": pd.np.nan}
    try:
        with open(stats_file) as handle:
            content = handle.readlines()  # list of strings per line
    except:
        return error_dict

    reads=pd.np.nan
    duplicates=pd.np.nan
    for line in content:
        match=re.match("([0-9]+) \+ 0 mapped \(.*\)",line)
        if (match):
            reads=int(match.group(1))
            continue

        match=re.match("([0-9]+) \+ 0 duplicates",line)
        if (match):
            duplicates=int(match.group(1))
            continue

    if (not pd.np.isnan(duplicates) and not pd.np.isnan(reads)):
        return {
            prefix + "mapped_reads": reads,
            prefix + "duplicate_percentage": (float(duplicates) / (reads) * 100)
        }
    else:
        return error_dict
        

def parse_peak_number(peak_file, prefix=""):
    try:
        return {prefix + "peaks": int(check_output(["wc", "-l", peak_file]).split(" ")[0])}
    except:
        return {prefix + "peaks": pd.np.nan}

def index_markdup_bam_file(tk,cpus,input_bam_file, output_bam_file, duplicate_stats):
    cmd1 = tk.tools.sambamba + " markdup -t {0} {1} {2}".format(cpus, input_bam_file,output_bam_file)
    cmd2 = "rm {0}".format(input_bam_file)
    cmd3 = tk.tools.sambamba + " index -t {0} {1}".format(cpus, output_bam_file)
    cmd4 = tk.tools.sambamba + " flagstat {0} > {1}".format(output_bam_file, duplicate_stats)
    
    return [cmd1, cmd2, cmd3, cmd4]

def get_mitochondrial_stats(tk, bam_file, output, cpus=4, mt_chrom="chrM"):
        cmd = "{0} slice {1} {2}|{0} flagstat /dev/stdin > {3}".format(tk.tools.sambamba, bam_file, mt_chrom, output)
        
        return cmd
    
def filter_reads(tk, input_bam, output_bam, metrics_file, paired=False, cpus=16, Q=30):
        """
        Remove duplicates, filter for >Q, remove multiple mapping reads.
        For paired-end reads, keep only proper pairs.
        """
        cmd1 = tk.tools.sambamba + ' view -t {0} -f bam --valid'.format(cpus)
        if paired:
            cmd1 += ' -F "not (unmapped or mate_is_unmapped) and proper_pair'
        else:
            cmd1 += ' -F "not unmapped'
        cmd1 += ' and not duplicate'
        cmd1 += ' and not (secondary_alignment or supplementary) and mapping_quality >= {0}"'.format(Q)
        cmd1 += ' {0} |'.format(input_bam)   
        cmd1 += tk.tools.sambamba + " sort -t {0} /dev/stdin -o {1}".format(cpus, output_bam)
        
        cmd2 = tk.tools.sambamba + " index -t {0} {1}".format(cpus, output_bam)
        cmd3 = tk.tools.sambamba + " flagstat {0} > {1}".format(output_bam, metrics_file)
        
        return [cmd1, cmd2, cmd3]

def calculate_frip(input_bam, input_bed, output, cpus=4):
    return ("sambamba view -t {0} -c  -L {1}  {2} > {3}"
            .format(cpus, input_bed, input_bam, output))


def parse_FRiP(coverage_file, total_reads, prefix=""):
    """
    Calculates the fraction of reads in peaks for a given sample.

    :param frip_file: A sting path to a file with the FRiP output.
    :type frip_file: str
    :param total_reads: A Sample object with the "peaks" attribute.
    :type total_reads: int
    """

    error_dict = {prefix + "frip": pd.np.nan}
    try:
        reads_in_peaks= pybedtools.BedTool(coverage_file).to_dataframe()

        reads_in_peaks = reads_in_peaks[reads_in_peaks.columns[-4]].astype(int).sum()
    except:
        return error_dict


    return {prefix + "frip": reads_in_peaks / float(total_reads)}


def parse_nsc_rsc(nsc_rsc_file):
    """
    Parses the values of NSC and RSC from a stats file.

    :param nsc_rsc_file: A sting path to a file with the NSC and RSC output (generally a tsv file).
    :type nsc_rsc_file: str
    """
    try:
        nsc_rsc = pd.read_csv(nsc_rsc_file, header=None, sep="\t")
        return {"NSC": nsc_rsc[8].squeeze(), "RSC": nsc_rsc[9].squeeze()}
    except:
        return {"NSC": pd.np.nan, "RSC": pd.np.nan}


def filter_peaks(peaks, exclude, filtered_peaks):
    return "bedtools intersect -v -wa -a {} -b {} > {}".format(
        peaks, exclude, filtered_peaks)


def bam_to_bigwig(
        input_bam, output_bigwig, genome,
        normalization_method="RPGC"):

    if genome not in ['hg19', 'hg38', 'mm10', 'mm9']:
        print("Genome assembly is not known. Using size of human genome. Beware.")

    genome_size = defaultdict(lambda: 3300000000)
    for g in ['mm9', 'mm10']:
        genome_size[g] = 2800000000

    cmd = "bamCoverage --bam {bam_file} -o {bigwig}"
    cmd += " -p max --binSize 10  --normalizeUsing {norm} --effectiveGenomeSize {genome_size} --extendReads 175"""
    cmd = cmd.format(bam_file=input_bam, bigwig=output_bigwig, norm=normalization_method, genome_size=genome_size[genome])
    return cmd

def calculate_transposition_events(
    input_bam,
    output_bed,
    chrom_file
):
    cmd = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'tools', 'extract_transp_events.py');
    cmd += " {} {} {}".format(input_bam, output_bed, chrom_file);
    return cmd;


def quantify(
    sample_bed,
    target_bed,
    output_bed,
    chrom_file
):
    cmd="bedtools coverage -a {} -b {}".format(target_bed,sample_bed)
    if (chrom_file):
        cmd+=" -sorted -g {}".format(chrom_file);
    cmd+=" > {}".format(output_bed)
    return cmd

def calculate_tss(
    input_bed,
    chrom_file,
    sample_name,
    target,
    out_folder
):
    script_to_run = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'tools', 'analyse_TSS.py');
    cmd = "python {script} -c {chrom_file} -s {sample_name} -o {out_folder} {input_bed} {target}"
    cmd = cmd.format(script=script_to_run,
                     chrom_file=chrom_file,
                     input_bed=input_bed,
                     sample_name=sample_name,
                     target=target,
                     out_folder=out_folder)
    return cmd

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("Program canceled by user!")
        sys.exit(1)
