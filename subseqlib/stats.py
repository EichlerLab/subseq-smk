"""
Subseq stats.
"""

import numpy as np
import pandas as pd

# Alignment summary table data types.
ALIGN_SUMMARY_FIELD_DTYPE = {
    'N': np.int32,
    'MEAN': np.float32,
    'MIN': np.int32,
    'MAX': np.int32,
    'N_LO': np.int32,
    'MEAN_LO': np.float32,
    'MIN_LO': np.int32,
    'MAX_LO': np.int32,
    'N_HI': np.int32,
    'MEAN_HI': np.float32,
    'MIN_HI': np.int32,
    'MAX_HI': np.int32,
    'DIST_LH': np.int32,
    'HAS_ALN': bool
}


#
# StepMiner
#

def step_miner(len_list):
    """
    Take a sorted list and split it into two sets (low and high) for each possible split (index = 1, 2, 3, ..., len(len_list)).
    For each set (low and high), compute the root-mean-squared error between the mean of the set and each element. For the split with
    the lowest error, the low and high lists are returned (tuple of two lists, low list is the first element, high list is the second).

    This StepMiner algorithm is borrowed from Debashis Sahoo's thesis:
    http://genedesk.ucsd.edu/home/dsahoo-thesis.pdf
    """

    min_index = None
    min_error = None

    n_list = len(len_list)

    if len(len_list) == 0:
        return [], [], 0, 0

    if len(len_list) == 1:
        return len_list, [], 0, 0

    # Get split with the least error
    for index in range(1, len(len_list)):

        len_low = len_list[:index]
        len_high = len_list[index:]

        mean_low = np.mean(len_low)
        mean_high = np.mean(len_high)

        error = (
            np.sum(np.abs(len_low - mean_low)**2) +
            np.sum(np.abs(len_high - mean_high)**2)
        )

        if error > 0:
            error = np.log2(error / n_list)

        if index == 1 or error < min_error:
            min_error = error
            min_index = index

    # Return splits
    return len_list[:min_index], len_list[min_index:], min_index, min_error

#
# Alignment summary record
#

def align_summary_haploid(len_list):
    
    # Get stats
    n = len(len_list)

    if n > 0:
        mean = np.mean(len_list)
        min = np.min(len_list)
        max = np.max(len_list)
    else:
        mean = 0
        min = 0
        max = 0

    # Return series
    return pd.Series(
        [
            n, mean, min, max,
            ','.join(['{:d}'.format(val) for val in len_list])
        ],
        index=[
            'N', 'MEAN', 'MIN', 'MAX',
            'LENS'
        ]
    )

def align_summary_diploid(len_list):

    len_low, len_high, min_index, min_error = step_miner(sorted(len_list))

    # Get stats
    n_low = len(len_low)
    n_high = len(len_high)

    if n_low > 0:
        mean_low = np.mean(len_low)
        min_low = np.min(len_low)
        max_low = np.max(len_low)
    else:
        mean_low = 0
        min_low = 0
        max_low = 0

    if n_high > 0:
        mean_high = np.mean(len_high)
        min_high = np.min(len_high)
        max_high = np.max(len_high)
    else:
        mean_high = 0
        min_high = 0
        max_high = 0

    if n_low > 0 and n_high > 0:
        separation = min_high - max_low
    else:
        separation = 0

    # Return series
    return pd.Series(
        [
            n_low, mean_low, min_low, max_low,
            n_high, mean_high, min_high, max_high,
            separation,
            ','.join(['{:d}'.format(val) for val in len_low]),
            ','.join(['{:d}'.format(val) for val in len_high])
        ],
        index=[
            'N_LO', 'MEAN_LO', 'MIN_LO', 'MAX_LO',
            'N_HI', 'MEAN_HI', 'MIN_HI', 'MAX_HI',
            'DIST_LH',
            'LENS_LO',
            'LENS_HI'
        ]
    )


