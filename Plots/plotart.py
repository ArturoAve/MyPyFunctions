#!/usr/bin/env python
# coding: utf-8
# Anaconda python 2.7

# Collection of functions to create frequent plots I usually need.
# This is my main "plotart.py" file.

#--------------------------------------------------------60
code_created_by = 'Arturo_Avelino'
# On date: 2019.01.10 (yyyy.mm.dd)
code_name = 'plotart.py'
version_code = '0.1.4'
last_update = '2019.04.23'

#--------------------------------------------------------60

from matplotlib import pyplot as plt
import numpy as np

##############################################################################80

#       ERROR BAR PLOT

def plot_errorbars(xx, yy, e_yy,
                xlim=[], ylim=[],
                color='red', fmt='.', ms=6, elinewidth=1, capsize=2, alpha=0.6,
                xlabel='x axis', ylabel='y axis',
                title = 'Data with error bars', fs=12,
                savefig = False,
                namesavefig = 'plot_data_errorbars_.png',
                resolution_dpi = 100,
                dir_save_output = ''):
    """
    Function to create a generic errorbar plot.

    NOTE: The created plot will be open [i.e., plt.figure()] or closed [i.e.,
    plt.close()] at the of running this function. This helps to use this
    function inside of a more complex creation of plots.
    So to create new plot with these functions, the first and last line should
    be plt.figure() and plt.close() respectively.

    Mandatory arguments:
        xx: the x data.
        yy: the y data.
        e_yy: the y data errors.

    Optional arguments:
        xlim: x-limits in the plot.
        ylim: y-limits in the plot.
        color: color of the datapoints.
        fmt: type of symbol to plot for the datapoints.
        ms: size of the symbols.
        elinewidth: width of the lines of the error bars.
        capsize: size of the ending lines of the error bars.
        fs: font size for the axis labels. Title is "fs+2".
        savefig: save the created plot?
        dir_save_output: directory to save the plot. The path to the directory
            should end with the "/" symbol.
        resolution_dpi: resolution of the plot file to be created.
    """

    # plt.figure()
    plt.errorbar(xx, yy, yerr = e_yy,
                fmt=fmt, color=color, ms=ms, alpha=alpha,
                elinewidth=elinewidth, capsize=capsize)

    plt.grid(True, ls='--', alpha=0.3)

    # x,y axes limits if defined by user:
    if len(xlim) > 0: plt.xlim(xlim[0], xlim[1])
    if len(ylim) > 0: plt.ylim(ylim[0], ylim[1])

    plt.xlabel(xlabel, fontsize=fs)
    plt.ylabel(ylabel, fontsize=fs)
    plt.title(title, fontsize=(fs+2))

    # plt.legend(loc='upper left')

    if savefig:
        plt.savefig(dir_save_output+namesavefig, dpi=resolution_dpi)

    # plt.close()
    # return plt.close()
    return '# Error bar plot created.'

#-----------------------------------------------------------------------------80

#       ERROR BAR PLOT: OVERPLOT 2 DATASETS

def plot_errorbars2(x1, y1, e_y1, x2, y2, e_y2,
                xlim=[], ylim=[],
                color1='blue', color2='red',
                alpha1=0.7, alpha2=0.5,
                fmt='.', ms=6, elinewidth=1, capsize=2,
                xlabel='x axis', ylabel='y axis',
                title = 'Data with error bars', fs=12,
                legend1='blue', legend2='red',
                legend_loc='upper right', legend_sizetext=10,
                savefig = False,
                namesavefig = 'plot_data_errorbars_.png',
                resolution_dpi = 100,
                dir_save_output = ''):
    """
    Function to create a generic errorbar plot.

    NOTE: The created plot will be open [i.e., plt.figure()] or closed [i.e.,
    plt.close()] at the of running this function. This helps to use this
    function inside of a more complex creation of plots.
    So to create new plot with these functions, the first and last line should
    be plt.figure() and plt.close() respectively.

    Mandatory arguments:
        (x1, y1, e_y1): the (x1, y1, e_y1) data.
        (x2, y2, e_y2): the (x2, y2, e_y2) data.

    Optional arguments:
        xlim: x-limits in the plot.
        ylim: y-limits in the plot.
        color: color of the datapoints.
        alpha: alpha transparency.
        fmt: type of symbol to plot for the datapoints.
        ms: size of the symbols.
        elinewidth: width of the lines of the error bars.
        capsize: size of the ending lines of the error bars.
        fs: font size for the axis labels. Title is "fs+2".
        savefig: save the created plot?
        dir_save_output: directory to save the plot. The path to the directory
            should end with the "/" symbol.
        resolution_dpi: resolution of the plot file to be created.
    """

    # plt.figure()
    plt.errorbar(x1, y1, yerr = e_y1,
                fmt=fmt, color=color1, ms=ms,
                elinewidth=elinewidth, capsize=capsize, alpha=alpha1,
                label=legend1)

    plt.errorbar(x2, y2, yerr = e_y2,
                fmt=fmt, color=color2, ms=ms,
                elinewidth=elinewidth, capsize=capsize, alpha=alpha2,
                label=legend2)

    plt.grid(True, ls='--', alpha=0.3)

    # x,y axes limits if defined by user:
    if len(xlim) > 0: plt.xlim(xlim[0], xlim[1])
    if len(ylim) > 0: plt.ylim(ylim[0], ylim[1])

    plt.xlabel(xlabel, fontsize=fs)
    plt.ylabel(ylabel, fontsize=fs)
    plt.title(title, fontsize=(fs+2))

    plt.legend(loc=legend_loc)

    if savefig:
        plt.savefig(dir_save_output+namesavefig, dpi=resolution_dpi)

    # plt.close()
    # return plt.close()
    return '# Overlay error bar plots created.'

#-----------------------------------------------------------------------------80

#           BAND PLOT

def plot_band(xx, yy, e_yy,
            xlim=[], ylim=[],
            color = 'g', alpha=0.8,
            xlabel='x axis', ylabel='y axis',
            title = 'Band plot', fs=12,
            savefig = False,
            namesavefig = 'plot_band_.png',
            resolution_dpi = 100,
            dir_save_output = ''):
    """
    Function to create a filled band plot.

    NOTE: The created plot will be open [i.e., plt.figure()] or closed [i.e.,
    plt.close()] at the of running this function. This helps to use this
    function inside of a more complex creation of plots.
    So to create new plot with these functions, the first and last line should
    be plt.figure() and plt.close() respectively.

    Mandatory arguments:
        xx: the x data.
        yy: the y data.
        e_yy: the y data errors for the band.

    Optional arguments:
        xlim: x-limits in the plot.
        ylim: y-limits in the plot.
        color: color of the datapoints.
        fs: font size for the axis labels. Title is "fs+2".
        savefig: save the created plot?
        dir_save_output: directory to save the plot. The path to the directory
            should end with the "/" symbol.
        resolution_dpi: resolution of the plot file to be created.
    """

    # Convert to an array of depth=2,required to create the plot
    xx1 = np.atleast_2d(xx).T

    # plt.figure()
    plt.fill(np.concatenate([xx1, xx1[::-1]]),
            np.concatenate([yy - 1. * e_yy,
                           (yy + 1. * e_yy)[::-1]]),
            alpha=alpha, fc=color, ec='None', label='band')

    plt.grid(True, ls='--', alpha=0.3)

    # x,y axes limits if defined by user:
    if len(xlim) > 0: plt.xlim(xlim[0], xlim[1])
    if len(ylim) > 0: plt.ylim(ylim[0], ylim[1])

    plt.xlabel(xlabel, fontsize=fs)
    plt.ylabel(ylabel, fontsize=fs)
    plt.title(title, fontsize=(fs+2))

    if savefig:
        plt.savefig(dir_save_output+namesavefig, dpi=resolution_dpi)

    # plt.close()
    return '# Plot band created.'


#-----------------------------------------------------------------------------80


#-----------------------------------------------------------------------------80

