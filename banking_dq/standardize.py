import numpy as np

def standardize_value(series, mapping):
    return series.str.upper().str.strip().replace(mapping).replace('', np.nan)