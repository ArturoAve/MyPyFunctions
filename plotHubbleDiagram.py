import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np

from sigmasSNeIa import sigma_mu_vpec
from distMuLCDM import DistanceMuVector

#--- ed values ---
cc = 299792.458  # Speed of light (km/s)

#--- Uncertainty in z_CMB:---
# Dan Scolnic gave me the value of err_cz_CMB = 150 km/s about the collection
# of z_CMB values he provided me.
err_cz_CMB = 150 # km/s.

err_zCMB_fix = err_cz_CMB/cc

#############################################################

def plotHD(zcmb, mu, err_mu, res_mu, sampleflag,
    sigmavpec = 150.0,
    OmM = 0.3, wcdm = -1.0, Ho = 70.,
    nameoutput = 'MyHubbleDiagram.png',
    dirsave = '', title = "Hubble diagram",
    saveinEPS = False,
    **kwargs):
    """
    :title: title of the plot to write on top of the figure.
    :saveinEPS: Save the plot in EPS format too.
    :param f: function to plot
    :type f: callable
    :param x: values for x
    :type x: list or ndarray

    Plots the distance moduli and residuals data in a Hubble diagram.
    """

    # old. title = kwargs.get('title','Preliminary RAISIN Hubble diagram')
    # old. dirsave = kwargs.get('dirsave', '')

    #############################################################

    # Some settings for plotting

    FontSize = 12

    #--- Plot range:
    xlimPlots = (min(zcmb)-0.01), (max(zcmb)+0.01)
    ylimPlots = (min(mu)-1.0), (max(mu)+1.0)
    ylimPlots_res = -1.0, 1.0

    #--- axes, title text ----------
    ylabel_HD = r'$\mu$'
    ylabel_res = r'$\mu - \mu_{\rm \Lambda CDM}$'
    xlabel = 'Redshift'

    #--- Data dots ------------
    MarkerSize = 6
    BarWidth = 1
    MyCapeSize = 2
    fmt_int = '.'

    #------------------------------------
    # Resolution to save the figure
    MyResolutionPlot = 300

    #--- Properites of the axis numbers
    SubtractAxisNumSize = 2 # 2

    Separation_x = 0.01
    loc_x_axis = np.arange(xlimPlots[0], xlimPlots[1], Separation_x)

    #############################################################

    # Theoretical (spectroscopic) distance modulus
    nbins1= 201
    zz_lcdm = np.linspace(0.001, 0.7, nbins1)
    mu_lcdm = DistanceMuVector(zz_lcdm, OmM, wcdm, Ho)

    # Array plot the peculiar velocity uncertanty curve
    error_zz = err_zCMB_fix * np.ones(len(zz_lcdm)) #
    sigma_pec_np = sigma_mu_vpec(zz_lcdm, error_zz, sigmavpec)
    mu0 = np.zeros(len(zz_lcdm)) # Array plot the residual line

    #############################################################

    fig = plt.figure(figsize=(6, 4))
    # fig = plt.figure()

    gs = gridspec.GridSpec(2, 1, height_ratios=[4,2])

    # Close the space between the subplots
    plt.subplots_adjust(wspace=0.002, hspace = 0.002)

    #############################################################

    ax1 = plt.subplot(gs[0])

    #              PLOT HUBBLE DIAGRAM

    for ii in range(len(mu)):

        sflag = sampleflag[ii]

        if sflag == 1:
            ax1.errorbar(zcmb[ii], mu[ii], yerr=err_mu[ii],
                         color='red', fmt=fmt_int,
                         ms=MarkerSize, elinewidth=BarWidth,
                         capsize=MyCapeSize)

        elif sflag == 2:
            ax1.errorbar(zcmb[ii], mu[ii], yerr=err_mu[ii],
                         color='blue', fmt=fmt_int,
                         ms=MarkerSize, elinewidth=BarWidth,
                         capsize=MyCapeSize)

        elif sflag == 3:
            ax1.errorbar(zcmb[ii], mu[ii], yerr=err_mu[ii],
                         color='green', fmt=fmt_int,
                         ms=MarkerSize, elinewidth=BarWidth,
                         capsize=MyCapeSize)

    #------------------------------------------------------

    # Plotting the LCDM theory line
    ax1.plot(zz_lcdm, mu_lcdm, color='black')


    # Write on the plot the LCDM cosmology values
    ax1.text(0.40, 40.5,
             r'$\Omega_{\rm M} = %.1f, \Omega_{\Lambda} = %.1f$, $\omega = %.1f$'%(
             OmM, (1.0-OmM), wcdm),
             fontsize=FontSize-2, color='black')

    #------------------------------------------------------

    ax1.text(0.25, 43.1,
             r'wRMS = $0.13 \pm 0.02$ ($\sigma_{\rm int} = 0.121 \pm 0.016$)',
              fontsize=FontSize-2, color='black')

    #------------------------------------------------------

    ax1.set_xlim(xlimPlots)
    ax1.set_ylim(ylimPlots)
    ax1.grid(ls='dashed', alpha=0.5)

    ax1.set_ylabel(ylabel_HD)
    ax1.set_title(title, fontsize=FontSize)

    #############################################################

    ax2 = plt.subplot(gs[1])

    #              PLOT HUBBLE RESIDUALS

    for ii in range(len(mu)):

        sflag = sampleflag[ii]

        if sflag == 1:
            ax2.errorbar(zcmb[ii], res_mu[ii], yerr=err_mu[ii],
                         color='red', fmt=fmt_int,
                         ms=MarkerSize, elinewidth=BarWidth,
                         capsize=MyCapeSize)

        elif sflag == 2:
            ax2.errorbar(zcmb[ii], res_mu[ii], yerr=err_mu[ii],
                         color='blue', fmt=fmt_int,
                         ms=MarkerSize, elinewidth=BarWidth,
                         capsize=MyCapeSize)

        elif sflag == 3:
            ax2.errorbar(zcmb[ii], res_mu[ii], yerr=err_mu[ii],
                         color='green', fmt=fmt_int,
                         ms=MarkerSize, elinewidth=BarWidth,
                         capsize=MyCapeSize)


    # Plotting the LCDM theory line
    ax2.plot(zz_lcdm, mu0, color='black')

    #------------------------------------------------------

    ax2.set_ylabel(ylabel_res)
    ax2.set_xlim(xlimPlots)
    ax2.set_ylim(ylimPlots_res)
    ax2.grid(ls='dashed', alpha=0.5)

    ax2.set_xlabel(xlabel)

    #############################################################

    plt.savefig(dirsave+nameoutput)
    if saveinEPS:
        plt.savefig(dirsave+nameoutput+'.eps', format='eps', dpi=300)
    # plt.savefig('Plot_HubbleDiagram_high.png', dpi=MyResolutionPlot)
    # plt.savefig('Plot_HubbleDiagram.eps', format='eps', dpi=300)

    plt.close()