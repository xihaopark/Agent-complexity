import os
import pybedtools as bedtools
from argparse import ArgumentParser
import pandas as pd
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

def get_enrichment(bed_file, tss_file,  chrom_file, output_folder, slop_size_event=25, slop_size=1000, bed_tmp=None, sample=None):
    if (bed_tmp is not None):
        bedtools.helpers.set_tempdir(bed_tmp)

    tss_bed=bedtools.BedTool(tss_file)
    tss_bed = tss_bed.slop(b=slop_size, g=chrom_file).sort(faidx=chrom_file)
    if (sample is None):
        sample = os.path.splitext(os.path.split(bed_file)[1])[0]
    
    output_base="{}_TSS".format(sample)
    alignments = bedtools.BedTool(bed_file).slop(g=chrom_file,b=slop_size_event).sort(faidx=chrom_file)
    
    coverage = tss_bed.coverage(alignments,g=chrom_file,sorted=True,d=True,F=0.5)
    
    histo = coverage.to_dataframe(names=['chrom','start','end','gene','X','strand','base','count'],usecols=['base','count','strand'])
    histo.loc[histo['strand']=='+','base'] = histo[histo['strand']=='+']['base']-slop_size-1
    histo.loc[histo['strand']=='-','base'] = -(histo[histo['strand']=='-']['base']-slop_size-1)
    histo=histo[['base','count']].sort_values(by=['base']).groupby('base').sum()
    
    noise = (histo[:100].sum()+histo[-100:].sum())/200
    norm_histo=histo/noise
    norm_histo.to_csv(os.path.join(output_folder,"{}.csv".format(output_base)))
    
    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(norm_histo.index, norm_histo, color='k')
    ax.axvline(0, linestyle=':', color='k')

    ax.set_xlabel('Distance from TSS (bp)')
    ax.set_ylabel('Normalized coverage')
    fig.savefig(os.path.join(output_folder,"{}.svg".format(output_base)))
    plt.close(fig)
    
    open(os.path.join(output_folder,"{}.complete".format(output_base)), 'w')
    
    print "TSS enrichment: {}".format(norm_histo.max())
    return norm_histo.max()


def main():
    parser = ArgumentParser()


    parser.add_argument("-c", "--chrom",
                        dest="chrom_file",
                        help="Chrom Size file",
                        default='hg38')
    
    parser.add_argument("-o", "--output",
                        dest="output_folder",
                        help="Output Folder",
                        default=".")
    
    parser.add_argument("-s", "--sample",
                        dest="sample_name",
                        help="Sample Name",
                        default=None)
    
    parser.add_argument('bed_file')
    parser.add_argument('tss_file')
    
    args = parser.parse_args()

    bed_file=args.bed_file
    if (not os.path.exists(bed_file)):
        print ("Bed File {} not found!".format(bed_file))
        return 1

    tss_file = args.tss_file
    if (not os.path.exists(tss_file)):
        print ("Bed File {} not found!".format(tss_file))
        return 1


    output_folder= args.output_folder
    if (not os.path.exists(output_folder)):
        os.makedirs(output_folder)

    get_enrichment(bed_file, tss_file, args.chrom_file,  output_folder, sample=args.sample_name)
    return 0

if __name__== "__main__":
    main()