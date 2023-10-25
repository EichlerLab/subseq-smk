###################
### Definitions ###
###################

#
# Parameters
#

# Reference reads and contgis were mapped against
REF_FA = '/net/eichler/vol26/eee_shared/assemblies/CHM13/T2T/v1.1/chm13_v1.1_plus38Y_masked.fasta'

# SV callers
SV_CALLER_LIST = [
    ('caller', 'extern-pav'),
    ('caller', 'extern-pavlra'),
    ('caller', 'pbsv-hifi')
]

# Samples
SAMPLES = [
      "HG002","HG00438","HG005","HG00621","HG00673","HG00733",
      "HG00735","HG00741","HG01071","HG01106","HG01109","HG01123",
      "HG01175","HG01243","HG01258","HG01358","HG01361","HG01891",
      "HG01928","HG01952","HG01978","HG02055","HG02080","HG02109",
      "HG02145","HG02148","HG02257","HG02486","HG02559","HG02572",
      "HG02622","HG02630","HG02717","HG02723","HG02818","HG02886",
      "HG03098","HG03453","HG03486","HG03492","HG03516","HG03540",
      "HG03579","NA18906","NA19240","NA20129","NA21309"
    ]

# Variant calls
VARIANT_BED_PATTERN = '/net/eichler/vol27/projects/hprc/nobackups/svpop/freeze1/chm13/results/variant/{source}/{caller}/bed/{sample}/all/chm13_lc/byref/sv_{svtype}.bed'

# Aligned data to validate against (reads and assemblies)
ALNSOURCE_PATTERN_DICT = {
    'hifi': '/net/eichler/vol27/projects/hprc/nobackups/variants/pbsv/pbsv_chm13_v1.1/align/{sample}/mapped_reads.bam'
}

# Location of the subseq script (extracts parts of aligned reads/contigs corresponding to a reference region and writes a FASTA)
SUBSEQ_EXE = '/net/eichler/vol27/projects/structural_variation/nobackups/tools/seqtools/201910/bin/subseqfa'

ALNSOURCE_PLOIDY_DICT = {
    'hifi': subseqlib.stats.align_summary_diploid
}

# SV tuples:
#   [0] Min svlen
#   [1] Max svlen (exclusive)
#   [2] Window (flank) bp
SET_DEF = {
    'sv50-100':
        (50, 100, 20),
    'sv100-200':
        (100, 200, 25),
    'sv200-500':
        (200, 500, 40),
    'sv500-1000':
        (500, 1000, 100),
    'sv1-2k':
        (1000, 2000, 200),
    'sv2-4k':
        (2000, 4000, 250),
    'sv4k-max':
        (4000, None, 300),
}
