from __future__ import absolute_import

import numpy as np
import matplotlib.pyplot as plt
from typing import List, Type

from thesisplots.tools import single_series_plot
from thesisplots.tools import Series, compare_and_shift, compare_superimpose


def _setup_raman():
    figure, axis = plt.subplots(1, 1)
    axis.set_xlabel('Raman shift [$cm^{-1}$]')
    axis.set_ylabel('Intensity [A.U]')
    return figure, axis


def _setup_ir():
    figure, axis = plt.subplots(1, 1)
    axis.set_ylabel('Absorbance [A.U]')
    axis.set_xlabel('Wavenumber [$cm^{-1}$]')
    return figure, axis


def raman(shift: Type[Series], image_filename: str):
    figure, axis = _setup_raman()
    single_series_plot(axis, shift)
    return (figure, axis, image_filename)


def raman_compare(series: List[Type[Series]], image_filename: str):
    figure, axis = compare_and_shift(_setup_raman, single_series_plot, series)
    return (figure, axis, image_filename)

def raman_compare_overlapped(series: List[Type[Series]], image_filename: str):
    figure, axis = compare_superimpose(_setup_raman, single_series_plot, series)
    return (figure, axis, image_filename)

def ir_compare(series: List[Type[Series]], image_filename: str):
    figure, axis = compare_and_shift(_setup_ir, single_series_plot, series)
    return (figure, axis, image_filename)

def debug_stack(figure):
    plt.setp([a.get_xticklabels() for a in figure.axes[:-1]], visible=True)

def _setup_vertical_panels(number_of_panels, gridspec_kw):
    #figure, axes = plt.subplots(number_of_panels)
    figure, axes = plt.subplots(number_of_panels, gridspec_kw=gridspec_kw)
    plt.setp([a.get_xticklabels() for a in figure.axes[:-1]], visible=False)
    return figure, axes


# http://stackoverflow.com/a/37150446/5179137
def set_shared_ylabel(figure, a, ylabel, labelpad = 0.01):
    """Set a y label shared by multiple axes
    Parameters
    ----------
    a: list of axes
    ylabel: string
    labelpad: float
        Sets the padding between ticklabels and axis label"""

    figure.canvas.draw() #sets f.canvas.renderer needed below

    # get the center position for all plots
    top = a[0].get_position().y1
    bottom = a[-1].get_position().y0

    # get the coordinates of the left side of the tick labels
    x0 = 1
    for at in a:
        at.set_ylabel('') # just to make sure we don't and up with multiple labels
        bboxes, _ = at.yaxis.get_ticklabel_extents(figure.canvas.renderer)
        bboxes = bboxes.inverse_transformed(figure.transFigure)
        xt = bboxes.x0
        if xt < x0:
            x0 = xt
    tick_label_left = x0

    # set position of label
    a[-1].set_ylabel(ylabel)
    a[-1].yaxis.set_label_coords(tick_label_left - labelpad,(bottom + top)/2, transform=figure.transFigure)


def raman_overtones(series, interval_start, panels_number, scalex, image_filename, debug_stacking=False):
    """Represent the Raman spectrum with a vertical stack in order to see the overtones
    
    series: the data to plot
    interval (int): the initial value
    panels_number (int): how many panels to stack
    scalex (float): scale the x values by this amount
    image_filename (str): the name for the image file
    debug_stacking (bool): if True, plot ticks and labels for each panel
    """
    gridspec_kw={'hspace':0}
    if debug_stacking:
        gridspec_kw={'hspace':1}
    figure, axes = _setup_vertical_panels(panels_number, gridspec_kw=gridspec_kw)
    if debug_stacking:
        debug_stack(figure)
    figure.set_size_inches((4, 4))
    #figure.set_tight_layout(True)
    #figure.subplots_adjust(hspace=0)
    for i in range(panels_number): # start at top and go down
        minimum = interval_start
        minimum = minimum*(2**i)
        maximum = 2*minimum
        axis_number = panels_number - i - 1
        axes[axis_number].set_xlim([minimum, maximum])
        single_series_plot(axes[axis_number], series, scalex)
        axes[axis_number].set_yticks([])
    plt.xlabel('Raman shift [$cm^{-1}$]')
    set_shared_ylabel(figure, axes, 'Intensity [A.U]')
    return (figure, axes, image_filename)
