"""
Sequence handling routines.
"""

import gzip
import io
import pandas as pd
import subprocess

from Bio import SeqIO

#
# Reference FAI Series
#

def get_ref_fai(fai_file_name):
    """
    Read a reference FAI file as a Series object of sequence lengths keyed by sequence name.
    """
    
    return pd.read_csv(
        fai_file_name,
        sep='\t',
        names=('CHROM', 'LEN', 'START', 'LEN_BP', 'LEN_BYTES'),
        usecols=('CHROM', 'LEN'),
        index_col='CHROM',
        squeeze=True
    )

def get_lengths(fa_file):
    """
    Get a list of record lengths for one input file.
    """

    with gzip.open(fa_file, 'rt') as in_file:
        return [len(record.seq) for record in SeqIO.parse(in_file, 'fasta')]

def get_len_list(window, aln_input, subseq_exe):
    """
    Get a list of alignment record lengths over a window.
    
    :param window: Position string (chrom:pos-end). Coordinates are 1-based inclusive (not BED).
    :param aln_input: Alignment input as BAM or CRAM.
    :param subseq_exe: Path to subseq executable.
    """
    
    # Open process
    proc = subprocess.Popen([subseq_exe, '-b', '-r', window, aln_input], stdout=subprocess.PIPE)

    stdout, stderr = proc.communicate()
    
    # Return list
    with io.StringIO(stdout.decode()) as in_file:
        return [len(record.seq) for record in SeqIO.parse(in_file, 'fasta')]
