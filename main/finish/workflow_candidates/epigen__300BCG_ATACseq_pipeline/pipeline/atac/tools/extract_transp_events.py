#!/usr/bin/env python
import sys
import pandas as pd
import pybedtools as bedtools

bam_file=sys.argv[1]
out_file=sys.argv[2]
chrom_file=sys.argv[3]

bed_file= bedtools.BedTool(bam_file).bam_to_bed()
df=bed_file.to_dataframe()

df.loc[df['strand']=='-','transp_end']=(df.loc[df['strand']=='-','end']-5).astype(int)
df.loc[df['strand']=='+','transp_end']=(df.loc[df['strand']=='+','start']+4).astype(int)
df['transp_end']=df['transp_end'].astype(int)
df['transp_start']=(df['transp_end']-1).astype(int)

bed_file= bedtools.BedTool().from_dataframe(
    df[['chrom','transp_start','transp_end','name','score','strand']]
).sort(faidx=chrom_file)

bed_file.saveas(out_file)