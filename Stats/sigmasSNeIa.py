# A collection of functions related to uncertainties (the "sigmas") commonly
# used in the analysis of SNeIa for cosmology.

import numpy as np

#--- Fixed values ---
cc = 299792.458  # Speed of light (km/s)

#--------------------------------------------------

def sigma_mu_vpec(zcmb, err_zcmb, sigma_vpec=150.0):
    """
    Uncertainty in the spectroscopic distance modulus due to the uncertainties
    in the peculiar velocity and redshift. See for instance Eq. (24) of
    Avelino+18.
    :sigma_vpec: uncertainty in the peculiar velocity. Default: 150.0 km/s.
    """
    sigma_mu_vpecInt = (5.0/(zcmb*np.log(10.0)) * np.sqrt( (sigma_vpec/cc)**2 +
                        err_zcmb**2) )
    return sigma_mu_vpecInt

#--------------------------------------------------
