"""
Validation functions.
"""

import numpy as np
import pandas as pd
import re

def validate_summary(df, strategy='size50_2_4'):
    """
    Run validation on. Generates a "VAL" colmun with:
    * VALID: 
    * NOTVALID: 
    * NOCALL: 
    * NODATA: 
    """
    
    # Get parameters
    match_obj = re.match(r'^size(\d+)_(\d+)_(\d+)$', strategy)
    
    if match_obj is None:
        raise RuntimeError('No implementation for strategy: ' + strategy)
    
    val_threshold = np.float32(match_obj[1]) / 100
    
    min_support = np.int32(match_obj[2])
    min_call_depth = np.int32(match_obj[3])
    
    # Subset df to needed columns
    df = df[['ID', 'SAMPLE', 'CALLER', 'ALNSAMPLE', 'ALNSOURCE', 'SVTYPE', 'SVLEN', 'LENS_HI', 'LENS_LO', 'HAS_ALN', 'WINDOW_SIZE']].copy()
    
    # Get lengths and SV length differences
    df['LEN'] = df.apply(lambda row:
        (row['LENS_LO'].split(',') if not pd.isnull(row['LENS_LO']) else []) +
        (row['LENS_HI'].split(',') if not pd.isnull(row['LENS_HI']) else []),
        axis=1
    )
    
    df['LEN_DIFF'] = df.apply(lambda row:
        [
            (int(val) - row['WINDOW_SIZE'] - (
                row['SVLEN'] if row['SVTYPE'] == 'INS' else 0)
            )
            for val in row['LEN']
        ] ,
        axis=1
    )
    
    # Count support
    df['SUPPORT_COUNT'] = df.apply(
        lambda row: np.sum(np.abs([
            np.int32(element) / row['SVLEN'] for element in row['LEN_DIFF']
        ]) < val_threshold),
        axis=1
    )
    
    # Call validation status
    df['VAL'] = df.apply(lambda row:
        (
            'VALID' if (row['SUPPORT_COUNT'] > min_support) else 'NOTVALID'
        ) if (
            len(row['LEN']) >= min_call_depth
        ) else 'NOCALL',
        axis=1
    )
        
    df['VAL'] = df.apply(lambda row: row['VAL'] if row['HAS_ALN'] else 'NODATA', axis=1)
    
    # Clean up
    del(df['LENS_HI'])
    del(df['LENS_LO'])
    del(df['LEN'])
    
    df['LEN_DIFF'] = df['LEN_DIFF'].apply(lambda vals: ','.join([str(val) for val in vals]))
    
    return df
