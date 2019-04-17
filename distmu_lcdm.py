# Functions to compute the spectroscopic cosmological distance modulus
# and luminosity distance.
# This is my main 'distmu.py' function.

#--------------------------------------------------------60
code_created_by = 'Arturo_Avelino'
# On date: 2017.04.15 (yyyy.mm.dd)
code_name = 'distmu.py'
version_code = '0.0.1'
last_update = '2019.04.15'
#--------------------------------------------------------60

import numpy as np
from scipy.integrate import quad as intquad

# Speed of light
cc = 299792.458  #  (km/s)

#--------------------------------------------------------60

# Inverse of the dimensionless Hubble parameter
def InvEHubblePar(z, OmM, wde=1.0):
    "Dimensionless Hubble parameter"
    InvEHubbleParInt = 1.0/(np.sqrt(OmM*(1.0+z)**3.0 + (1.0-OmM)*(1.+z)**(3.*(1.+wde))))
    return InvEHubbleParInt

# ---- The luminosity distance ----
def LumDistanceVec(z=0.0, OmM=0.27, wde=1.0, Ho=72.0):
    "Luminosity distance"
    LumDistanceVecInt = 0.
    LumDistanceVecInt = cc*(1.+z)*intquad(InvEHubblePar, 0., z, args=(OmM, wde))[0]/Ho
    return LumDistanceVecInt

# ---- Distance modulus scalar ----
def DistanceMu(z, OmM=0.27, wde=1.0, Ho=72.0):
    "Distance modulus"
    DistanceMuInt = 5.0*np.log10(LumDistanceVec(z, OmM, wde, Ho)) + 25.0
    return DistanceMuInt

# ---- Distance modulus Vector ----
def DistanceMuVector(z, OmM=0.27, wde=1.0, Ho=72.0):
    "Distance modulus"
    DistanceMuInt= []
    for i in range(len(z)):
        DistanceMuInt += [5.0*np.log10(LumDistanceVec(z[i], OmM, wde, Ho)) + 25.0]
    return DistanceMuInt
