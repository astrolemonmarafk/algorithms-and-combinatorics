import numpy as np

def ranp(n=30, seed=None): # Random Points
    if seed is not None:
        np.random.seed(seed)
    return [tuple(p) for p in np.random.rand(n, 2)]

def fcsvp(filepath): # Points from CSV
    import pandas as pd
    df = pd.read_csv(filepath)
    return list(zip(df['x'], df['y']))

def cosp(): # Custom Example
    return [(0,0), (1,1), (2,2), (2,0), (2,4), (3,3), (0,3)]
