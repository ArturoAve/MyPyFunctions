# Functions to compute the spectroscopic cosmological distance modulus
# and luminosity distance.
# This is my main 'distmu.py' function.

#--------------------------------------------------------60
code_created_by = 'Arturo_Avelino'
# On date: 2017.04.15 (yyyy.mm.dd)
code_name = 'intrinsic_scatter.py'
version_code = '0.0.1'
last_update = '2019.04.15'
#--------------------------------------------------------60

import numpy as np
from scipy.optimize import fmin as simplex

#--------------------------------------------------------60

# Finding the best estimated value for sigma2Pred by minimizing the
# -2ln(Likelihood) function, Eq. (B.6) of Blondin et al 2011.

def neg2lnLikelihood(intrinsic_scatter, residuals_np, s_peculiar_vel_np,
                    s_appmagTBmax_np):
    """
    -2*log(Likelihood) function to minimized to compute the intrinsic scatter
        from the Hubble residuals. This Likelihood function comes from Eq. (6)
        of Blondin et al 2011.
    :param intrinsic_scatter : the intrinsic scatter.
    :type intrinsic_scatter : float.
    :param residuals_np : numpy array of Hubble residuals.
    :type residuals_np : ndarray.
    :param s_peculiar_vel_np : numpy array of peculiar-velocity uncertainties.
    :type s_peculiar_vel_np : ndarray.
    :param s_appmagTBmax_np : numpy array of apparent magnitude at t_Bmax
        uncertainties.
    :type s_appmagTBmax_np : ndarray.
    """
    sum1 = 0
    for i in range(len(residuals_np)):
        sum1 = (sum1 + np.log(s_appmagTBmax_np[i]**2 + intrinsic_scatter**2 +
        s_peculiar_vel_np[i]**2) +
        (residuals_np[i]**2)/(s_appmagTBmax_np[i]**2 + intrinsic_scatter**2 +
        s_peculiar_vel_np[i]**2 ) )
    return sum1

def scatter(residuals_np, s_peculiar_vel_np, s_appmagTBmax_np, InitialGuess=0.15):
    """
    Function to compute the intrinsic scatter from the Hubble residuals by
        minimizing the -2*log(Likelihood) function in Eq. (6) of Blondin et al 2011.
    :param residuals_np : numpy array of Hubble residuals.
    :type residuals_np : ndarray.
    :param s_peculiar_vel_np : numpy array of peculiar-velocity uncertainties.
    :type s_peculiar_vel_np : ndarray.
    :param s_appmagTBmax_np : numpy array of apparent magnitude at t_Bmax
        uncertainties.
    :type s_appmagTBmax_np : ndarray.
    :param InitialGuess : Initial guess about the value of the intrinsic scatter.
        Default value = 0.15.
    :type InitialGuess : float.
    """
    int_scatter = simplex(neg2lnLikelihood, InitialGuess,
                            args=(residuals_np, s_peculiar_vel_np,
                             s_appmagTBmax_np))
    return int_scatter[0]

#--------------------------------------------------------60

#   Uncertainty on the intrinsic scatter best estimate

# Define the Fisher information matrix, Eq. (B.7) of Blondin et al 2011
def FisherFunc(intrinsic_scatter, residuals_np, s_peculiar_vel_np,
                s_appmagTBmax_np):
    """
    Function to compute the Fisher information matrix, Eq. (B.7) of
        Blondin et al 2011.
    :param intrinsic_scatter : the intrinsic scatter.
    :type intrinsic_scatter : float.
    :param residuals_np : numpy array of Hubble residuals.
    :type residuals_np : ndarray.
    :param s_peculiar_vel_np : numpy array of peculiar-velocity uncertainties.
    :type s_peculiar_vel_np : ndarray.
    :param s_appmagTBmax_np : numpy array of apparent magnitude at t_Bmax
        uncertainties.
    :type s_appmagTBmax_np : ndarray.
    """
    sum2 = 0
    for i in range(len(residuals_np)):
        sum2 = (sum2 + (residuals_np[i]**2)/(s_appmagTBmax_np[i]**2 +
                intrinsic_scatter**2 + s_peculiar_vel_np[i]**2)**3 -
               1.0/( 2.0*(s_appmagTBmax_np[i]**2 + intrinsic_scatter**2 +
                    s_peculiar_vel_np[i]**2 )**2 )  )
    return sum2


def error_intscatter(intrinsic_scatter, residuals_np, s_peculiar_vel_np,
                    s_appmagTBmax_np):
    """
    Function to uncertainty in the intrinsic dispersion.
    :param intrinsic_scatter : the intrinsic scatter.
    :type intrinsic_scatter : float.
    :param residuals_np : numpy array of Hubble residuals.
    :type residuals_np : ndarray.
    :param s_peculiar_vel_np : numpy array of peculiar-velocity uncertainties.
    :type s_peculiar_vel_np : ndarray.
    :param s_appmagTBmax_np : numpy array of apparent magnitude at t_Bmax
        uncertainties.
    :type s_appmagTBmax_np : ndarray.
    """
    square_sigma = 1.0/FisherFunc(intrinsic_scatter,
                                residuals_np, s_peculiar_vel_np,
                                s_appmagTBmax_np)

    return np.sqrt(square_sigma /(4.0*intrinsic_scatter**2))
