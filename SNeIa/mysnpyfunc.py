#
#       MY SNOOPY FUNCTIONS
#
#--------------------------------------------------------60
code_created_by = 'Arturo_Avelino'
# On date: '2019.06.17' (yyyy.mm.dd)
code_name = 'mysnpyfunc.py'
code_version = '0.1.9'
last_update = '2019.11.01'

#--------------------------------------------------------60

from snpy import *
from matplotlib import pyplot as plt
import numpy as np
import datetime # Get the current date and time
import random # To compute k-corr uncertainties
import json # To save the simulated mag and k-corr uncertainties.
import traceback # To print exception error in the try/except command.

##############################################################################80

def snpyfit(sn_filename, bands_to_fit=[], obs_rest_bands=[],
            apply_kcorr=True, mangled_kcorr=True, kc_uncertainty=False,
            apply_stretch=True, NumSim=100,
            Ho_value=72.0, dir_save_output='', num_char_trim=-11,
            debug=False, model='EBV_model', dpi_filters=60, **args):
    """
    Function to fit the light-curve data of a SINGLE supernova, create and
    save the fit plot, and summary of the results.

    bands_to_fit (list): specific observer-frame bands to fit.

    obs_rest_bands (list): specific observer-frame bands that I want
        to fit using specific restframe bands defined in rest_bands.
        The first and second filters in the sublists are the
        observer and rest frames bands respectively.
        For example:

                    obs_rest_bands = [[f125w, Y], [f160w, J]]

    num_char_trim (int): number of characters to trim at the end of the file
        name to save the output files

    model (str): specify the SNooPy model to use to fit the data.
        Options: ('EBV_model', 'EBV_model2', 'max_model')

    dpi_filters (int): dpi resolution of the filter's plot.

    **args: Any additional arguments for s.fit(), for instance, Tmax, bands

    """

    if debug: print('#- Try to upload the file: %s.'%sn_filename)
    s = get_sn(sn_filename)
    if debug: print('#- File uploaded sucessfully.')

    # Specify the SNooPy model to use to fit the data:
    if debug: print('#- Try to specify the SNooPy model %s.'%model)
    # s.choose_model(model)
    if model is not 'EBV_model': s.choose_model(model)
    if debug: print('#- SNooPy %s model specified sucessfully.'%model)

    # Supernova name to use to save the output files:
    snname_save = sn_filename[:num_char_trim]

    if debug: print('#- %s LC data: uploaded.'%sn_filename)

    # Define the restframe bands if indicated to do so for some
    # particular observer frame bands:
    if len(obs_rest_bands) > 0:
        for i1 in range(len(obs_rest_bands)):
            s.restbands[obs_rest_bands[i1][0]] = obs_rest_bands[i1][1]

    #-------------------------------------
    #             FITTING

    BandsToFit = []; # reset

    # Fit the data based on the specified filters:
    if len(bands_to_fit) > 0:

        # Create a list with the specific band names to fit for this SN:
        # old. for band1 in s.data.keys():
        for band1 in bands_to_fit:
            if band1 in s.data.keys(): BandsToFit += [band1]

        print('#-',BandsToFit)

        if debug: print('#- List with the specific band names to fit: created.')

        # FIT
        s.fit(bands=BandsToFit, mangle=mangled_kcorr,
              dokcorr=apply_kcorr, k_stretch=apply_stretch,
              reset_kcorrs=True, **args)

    else:
        # FIT
        s.fit(mangle=mangled_kcorr,
              dokcorr=apply_kcorr, k_stretch=apply_stretch,
              reset_kcorrs=True, **args)

        BandsToFit = s.data.keys()


    if debug: print('#- %s: FITTED.'%sn_filename)

    #-------------------------------------
    #  Saving the snpy data

    s.save(dir_save_output+snname_save+'_Fit.snpy')

    if debug: print("#- 'snpy' file: saved.")

    #-------------------------------------
    # Save fitted LC plot but with no text

    s.plot(epoch=True, outfile=dir_save_output+snname_save+'_PlotFit.png')
    plt.close()
    if debug: print('#- Plot with no text: done and saved.')

    #-------------------------------------
    # Save fitted LC plot WITH text

    s.plot(epoch=True) # Epoch for time axis

    # Determine the y location for the text info. It is going to be
    # below (1.5 mag) from the maximum of the first filter to be plotted
    try:
        yLoc = s.get_max(bands=BandsToFit[0])[1]+0.8
    except:
        yLoc = s.get_max(bands=s.filter_order[1])[1]+0.8

    if model=='EBV_model':
        plt.text(0, yLoc, r"$\Delta$m15 = %.2f $\pm$ %.2f"%(s.dm15,s.e_dm15),
                 color="black", fontsize=10)

    elif model=='EBV_model2':
        plt.text(0, yLoc, r"Stretch = %.2f $\pm$ %.2f"%(s.st,s.e_st),
                 color="black", fontsize=10)

    plt.text(0, yLoc+0.6, r"$z_{\rm hel}$ = %.3f" %(s.z),
                color="black", fontsize=10)
    plt.text(0, yLoc+1.2, r"$\mu$ = %.3f $\pm$ %.3f"%(s.DM,s.e_DM),
                color="black", fontsize=10)
    plt.text(0, yLoc+1.8, r"$T_{\rm Bmax}$ = %.2f $\pm$ %.3f"%(s.Tmax,s.e_Tmax),
                color="black", fontsize=10)
    plt.text(0, yLoc+2.4, r"E(B-V)$_{\rm host}$ = %.3f $\pm$ %.3f"%(
                    s.EBVhost,s.e_EBVhost),
                color="black", fontsize=10)
    plt.text(0, yLoc+3.0, r"E(B-V)$_{\rm MW}$ = %.3f $\pm$ %.4f "%(
                    s.EBVgal, s.e_EBVgal),
                color="black", fontsize=10)

    plt.savefig(dir_save_output+snname_save+'_PlotFitText.png', dpi=90)
    plt.close()

    if debug: print('#- Plot with text: done and saved.')

    #-------------------------------------
    # Overplot plot

    s.plot(epoch=True, single=True, offset=1,
           outfile=dir_save_output+snname_save+'_PlotOver.png')
    plt.close()
    if debug: print('#- Plot overlay: done and saved.')

    #-------------------------------------
    # k-correction plots

    s.plot_kcorrs(outfile=dir_save_output+snname_save+'_PlotKcorrs.png')
    plt.close()
    if debug: print('#- Plot k-corrections: done and saved.')

    #-------------------------------------
    # Plot filters

    s.plot_filters(fill=True, outfile=dir_save_output+snname_save+'_Filters.png',
                    dpi=dpi_filters)
    plt.close()
    if debug: print("#- Plot filters: done and saved.")

    #-------------------------------------
    # Save summary to a text file.

    s.summary(textFileOut=dir_save_output+snname_save+'_SummaryFit_.txt')

    #---------------
    # Append metadata to the summary file.

    text_line = '#'+'-'*57 + '60\n'

    now = datetime.datetime.now() # Read the time and date right now
    text_timenow = now.strftime("%Y.%m.%d (yyyy.mm.dd); %H:%M hrs.")
    text_Date   = '# On date: %s \n'%text_timenow
    text_Author = '# Data table created by: %s\n'%code_created_by
    text_script = '# Script used: %s (version %s | last update: %s)\n'%(
        code_name, code_version, last_update)

    if debug: print('#- Time, date, author, script: defined.')

    textfile_1 = open(dir_save_output+snname_save+'_SummaryFit_.txt','a')
    textfile_1.write(text_line)
    textfile_1.write('# SNooPy model used to fit: %s\n'%model)
    textfile_1.write('# Specified bands to fit: %s\n'%bands_to_fit)
    textfile_1.write("# Fitted bands: %s\n"%BandsToFit)
    textfile_1.write('# Specified match among observed to restframe bands: \
%s\n'%obs_rest_bands)
    textfile_1.write('# apply_kcorr = %s\n'%apply_kcorr)
    textfile_1.write('# mangled_kcorr = %s\n'%mangled_kcorr)
    textfile_1.write('# apply_stretch = %s\n'%apply_stretch)
    textfile_1.write('# Ho_value = %s\n'%Ho_value)
    textfile_1.write(text_line)

    textfile_1.write(text_Author)
    textfile_1.write(text_Date)
    textfile_1.write(text_script)
    textfile_1.close()

    if debug: print('#- Summary text file: done and saved.')

    #===========================================================================

    #      Compute k-correction uncertainties

    if kc_uncertainty:

        if debug: print("#- I'm going to compute k-corr uncertainties.")

        # Creating a dictionary with the original magnitude data of fitted bands
        errmag_fix_dict = {} # error_mag dictionary for all bands
        mag_dict = {} # mag dict to store all the simulated photometry

        # kcorr values dictionary to store all the data for all random draws.
        # Copying the original kcorr dictionary to initialize the dictionary
        kcorr_dict = {} # To add the simulated kcorr values.

        for band3 in BandsToFit:
            mag_dict[band3+'_0'] = list(s.data[band3].mag) # original mag data
            errmag_fix_dict[band3] = s.data[band3].e_mag # original e_mag data
            kcorr_dict[band3+'_0'] = list(s.ks[band3]) # original kcorr data

        if debug:
            print("#- Create initial mag, err_mag, kcorr, dictionaries: OK")

        #----- Main loop to estimate k-corr uncertainties ------->>
        # This part may take few minutes to run for each SN

        print("#- Simulating %s times the photometry and computing their \
k-corrections."%(NumSim))
        print('#- Loop step:', end='')

        for j2 in range(NumSim): # Loop over simulations
            for band5 in BandsToFit: # Loop over bands.
                # Loop over photometry in a given band.
                for i2 in range(len(s.data[band5].mag)):

                    muInt = 0; sigmaInt=0; # initialize these values.

                    # Defining a single datum from the original data:
                    muInt = mag_dict[band5+'_0'][i2]
                    sigmaInt = errmag_fix_dict[band5][i2]

                    # Generate Gaussian random photometry and redefine it
                    # as the "actual" photometry.
                    mag_sim_int = random.gauss(muInt, sigmaInt)
                    s.data[band5].mag[i2] = mag_sim_int

            # Fit the simulated photometry in order to generate the new
            # kcorrection values. The advantage of fitting the simulated photometry
            # instead of just k-correcting it is that it allows to interpolate
            # the dates with no data to BETTER derive colors and then more
            # precise k-corr uncertainties.
            #
            s.fit(bands=BandsToFit, mangle=mangled_kcorr,
                  dokcorr=apply_kcorr, k_stretch=apply_stretch,
                  reset_kcorrs=True, **args)

            # Save the new kcorr values and simulated magnitudes to the
            # "kcorr_dict" and "mag_dict" dicts.
            for band6 in BandsToFit:
                kcorr_dict[band6+'_%s'%(j2+1)] = list(s.ks[band6])
                mag_dict[band6+'_%s'%(j2+1)] = list(s.data[band6].mag)

            # Print the loop step number:
            if debug: print(", %s"%j2, end='') #
        # <<--- end main loop for k-corr uncertainties

        if debug:
            print('\n#- k-corr uncertainties computed OK. Now save the simulation.')

        # Create a dictionary with the mean and standard deviation of the kcorr values
        # at a given MJD for a given band.
        meanStd_kcorr_dict = {}

        for band7 in BandsToFit: # Loop over bands.
            meanStd_kcorr_dict[band7] = {}
            for i4 in range(len(s.data[band7].MJD)): # Loop over MJD for a given band.
                MJD_int = s.data[band7].MJD[i4] # Define the MJD.
                # Loop over simulations for a given MJD and band.
                meanStd_kcorr_dict[band7][str(MJD_int)] = [
                mean(np.array([kcorr_dict[band7+'_%s'%j3][i4] for j3 in range(NumSim+1) ])),
                std(np.array([kcorr_dict[band7+'_%s'%j3][i4] for j3 in range(NumSim+1) ])) ]

        #--- Saving the dictionaries created above above using JSON format ---

        # Dictionary of Monte-Carlo simulated k-corrs
        with open(dir_save_output+snname_save+'_sim_kcorr.json', 'w') as outfile:
            json.dump(kcorr_dict, outfile, sort_keys=True, indent=4)

        # Dictionary of simulated photometry.
        with open(dir_save_output+snname_save+'_sim_mag.json', 'w') as outfile:
            json.dump(mag_dict, outfile, sort_keys=True, indent=4)

        # Dictionary of mean and standard deviation.
        with open(dir_save_output+snname_save+'_sim_kcorr_Mean_Std.json', 'w') as outfile:
            json.dump(meanStd_kcorr_dict, outfile, sort_keys=True, indent=4)

        if debug:
            print("#- Simulation to determine k-corr uncertainties saved \
to JSON files.")

        #--------------------PLOTS SIMULATIONS ---------------------------------

        #            Plot  simulated photometry

        # Dictionary of colors:
        color_dict ={
            'g_ps1':['b','o'],
            'g_des':['b','o'],
            'r_ps1':['green','+'],
            'r_des':['green','+'],
            'i_ps1':['gold','x'],
            'i_des':['gold','x'],
            'z_ps1':['orange','<'],
            'z_des':['orange','<'],
            'f125w':['red','*'],
            'f160w':['salmon','>']}

        # factor to separate the bands in the plot
        factor_separate_band8 = 3.0;

        plt.clf(); plt.close() # clearing previous plot.
        plt.figure() # Start a new plot.

        count_band8 = 0 # reset
        for band8 in BandsToFit: # Loop over fitted bands.
            # Plot the simulated photometry in a given band
            for j4 in range(NumSim): # Loop over simulated datasets

                # Convert to a numpy array:
                array8 = np.array(mag_dict[band8+'_%s'%(j4+1)])

                # Shift the magnitudes vertically to better overplot the
                # data in for all the bands:
                array8_1 = array8 + (count_band8 * factor_separate_band8)

                # old. plt.plot((s.data[band8].MJD-s.Tmax)/((1+s.z)*s.ks_s),
                plt.plot((s.data[band8].MJD-s.Tmax), array8_1,
                         ls='', marker = color_dict[band8][1],
                         color=color_dict[band8][0], ms=5,
                         # markeredgecolor = 'None',
                         alpha=0.3)

            # Plot name of the bands:
            array8_2 = (np.array(mag_dict[band8+'_0']) +
                        (count_band8 * factor_separate_band8) )

            plt.text(-12, min(array8_2), '%s + %s'%
                                  (band8, count_band8 * factor_separate_band8),
                     color=color_dict[band8][0], )

            count_band8 += 1 # count bands

        plt.ylim( max(mag_dict[BandsToFit[-1]+'_0'] ) +
                        (0.5+(count_band8*factor_separate_band8)),
                  min(mag_dict[BandsToFit[0]+'_0']) - 2.5 )

        plt.title('%s. Simulated photometry'%s.name, fontsize=10)
        plt.xlabel('Epoch (observer-frame days)')
        plt.ylabel('magnitude')
        plt.tight_layout()

        plt.savefig(dir_save_output+snname_save+'_sim_LCs.png', dpi=110)
        plt.close()

        #-------------------------------------------------
        #       Plot k-corrections from the simulated photometry

        # factor to separate the bands in the plot
        factor_separate_band9 = 0.5;

        plt.clf(); plt.close() # clearing previous plot.
        plt.figure() # Start a new plot.

        count_band9 = 0 # reset
        for band9 in BandsToFit: # Loop over fitted bands.
            # Plot the simulated photometry in a given band
            for j5 in range(NumSim): # Loop over simulated datasets

                # Convert to a numpy array:
                array9 = np.array(kcorr_dict[band9+'_%s'%(j5+1)])

                # Shift the magnitudes vertically to better overplot the
                # data in for all the bands:
                array9_1 = array9 + (count_band9 * factor_separate_band9)

                # old. plt.plot((s.data[band9].MJD-s.Tmax)/((1+s.z)*s.ks_s),
                plt.plot((s.data[band9].MJD-s.Tmax), array9_1,
                         ls='', marker = color_dict[band9][1],
                         color=color_dict[band9][0], ms=5,
                         # markeredgecolor = 'None',
                         alpha=0.3)

            # Plot name of the bands:
            array9_2 = (np.array(kcorr_dict[band9+'_0']) +
                        (count_band9 * factor_separate_band9) )

            plt.text(12, min(array9_2), '%s + %.2f'%
                                  (band9, count_band9 * factor_separate_band9),
                     color=color_dict[band9][0], )

            count_band9 += 1 # count bands

        plt.title('%s. K-corrs from simulated photometry'%s.name,
                fontsize=10)
        plt.xlabel('Epoch (observer-frame days)')
        plt.ylabel('magnitude')
        plt.tight_layout()

        plt.savefig(dir_save_output+snname_save+'_sim_kcorr.png', dpi=110)
        plt.close()


    else: print("#- No kcorr uncertainties computed.")

    #===========================================================================

    print('#- %s fitted with no issues.\n'%snname_save)

    return '#---- %s done ----'%snname_save

#-----------------------------------------------------------------------------80
