#!/usr/bin/env python
# coding: utf-8
# Anaconda python 2.7

# Collection of functions to fit a line to data
# This is my MAIN "plotart.py" file.

#--------------------------------------------------------60
code_created_by = 'Arturo_Avelino'
# On date: 2019.05.14 (yyyy.mm.dd)
code_name = 'fitline.py'
code_version = '0.0.1'
code_last_update = '2019.05.14'

#--------------------------------------------------------60

from matplotlib import pyplot as plt
import numpy as np

##############################################################################80

##              Generative model (GM)
## Using the complete generative model approach to
## determine best estimated values of the slope, intercept, and goodness of fit,
## of a line that fit the data accounting for outliers properly.
## See "Data analysis recipes: Fitting a model to data"
## David W. Hogg, Jo Bovy, Dustin Lang, 2010
## arXiv:1008.4686 https://arxiv.org/abs/1008.4686

#--------------------------------------------------------60

# Log-likelihood function
#
# NOTE: Given that the range of values for Vb is huge, I have redefined the variable Vb as "eVb",
# so that the actual variance is Vb = exp(eVb).

def lnLikelihood(m, b, Pb, Yb, eVb):
    'The ln(likelihood) function'

    lnProducInt = 0.0

    for i in range(len(dm15_zcut)):
        lnProducInt = lnProducInt + np.log(((1.-Pb)/np.sqrt(2.*np.pi*(M0error_zcut[i]**2.)))*np.exp(-((M0_zcut[i]-m*dm15_zcut[i]-b)**2.)/(2.*M0error_zcut[i]**2.))
                                           + (Pb/np.sqrt(2.*np.pi*(np.exp(eVb)+M0error_zcut[i]**2.)))*np.exp(-((M0_zcut[i]-Yb)**2.)/(2.*(np.exp(eVb)+M0error_zcut[i]**2.))))
    return lnProducInt

lnLikelihood(0.4, -18.91, 0.25, -18.5, 1)

#---------

# lnLikelihood(0.4, -18.91, 0.25, -18.5, 1)
# 3.5549744860761896
# -15.311479267461962


#--------------------------------------------------------60