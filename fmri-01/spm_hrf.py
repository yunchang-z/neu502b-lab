#!/usr/bin/env python
from __future__ import division
import numpy as np
from scipy.stats import gamma

def spm_hrf(TR, t1=6, t2=16, d1=1, d2=1, ratio=6, onset=0, kernel=32):
    """Python implementation of spm_hrf.m from the SPM software.
    
    Parameters
    ----------
    TR : float
        Repetition time at which to generate the HRF (in seconds)
    t1 : float (default=6)
        Delay of response relative to onset (in seconds)
    t2 : float (default=16)
        Delay of undershoot relative to onset (in seconds)
    d1 : float (default=1)
        Dispersion of response
    d2 : float (default=1)
        Dispersion of undershoot
    ratio : float (default=6)
        Ratio of response to undershoot
    onset : float (default=0)
        Onset of hemodynamic response (in seconds)
    kernel : float (default=32)
        Length of kernel (in seconds)

    Returns
    -------
    hrf : array
        Hemodynamic repsonse function
    
    References
    ----------
    [1] Adapted from the Poldrack lab fMRI tools.
        https://github.com/poldracklab/poldracklab-base/blob/master/fmri/spm_hrf.py
    """

    ## Define metadata.
    fMRI_T = 16.0
    TR = float(TR)
    
    ## Define times.
    dt = TR/fMRI_T
    u  = np.arange(kernel/dt + 1) - onset/dt
    
    ## Generate (super-sampled) HRF.
    hrf = gamma(t1/d1,scale=1.0/(dt/d1)).pdf(u) - gamma(t2/d2,scale=1.0/(dt/d2)).pdf(u)/ratio
    
    ## Downsample.
    good_pts=np.array(range(np.int(kernel/TR)))*fMRI_T
    hrf=hrf[good_pts.astype(int)]
    
    ## Normalize and return.
    hrf = hrf/np.sum(hrf)
    return hrf
