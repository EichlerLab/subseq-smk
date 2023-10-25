"""
Pipeline functions. Mainly routines for finding input data.
"""

import os

def get_variant_input(wildcards, bed_pattern, allow_missing=False):
    """
    Get an input file name if it exists.
    """
    
    if '{source}' not in bed_pattern:
        raise RuntimeError('{source} not in BED pattern')
    
    if '{caller}' not in bed_pattern:
        raise RuntimeError('{caller} not in BED pattern')
    
    if '{sample}' not in bed_pattern:
        raise RuntimeError('{sample} not in BED pattern')
    
    if '{svtype}' not in bed_pattern:
        raise RuntimeError('{svtype} not in BED pattern')
    
    bed_file_name = bed_pattern.format(**wildcards)
    
    if not os.path.isfile(bed_file_name):
        if allow_missing:
            return []
        
        raise RuntimeError('Missing BED file: {}'.format(bed_file_name))
    
    return bed_file_name

def get_aln_source(wildcards, alnsource_pattern_dict):
    """
    Get an alignment source (BAM, CRAM) for a sample.
    """
    
    if wildcards.alnsource not in alnsource_pattern_dict:
        raise RuntimeError('Cannot find alignment source "{}" in alignment source pattern dictionary'.format(wildcards.alnsource))
    
    alnsource_pattern = alnsource_pattern_dict[wildcards.alnsource]
    
    if '{sample}' not in alnsource_pattern:
        raise RuntimeError('{{sample}} not in alignment source pattern: {}'.format(wildcards.alnsource))
    
    return alnsource_pattern.format(sample=wildcards.alnsample)
