from __future__ import absolute_import

import numpy as np
import matplotlib.pyplot as plt
from typing import List, Type

from thesisplots.tools import single_series_plot
from thesisplots.tools import Series, compare_and_shift


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


def ir_compare(series: List[Type[Series]], image_filename: str):
    figure, axis = compare_and_shift(_setup_ir, single_series_plot, series)
    return (figure, axis, image_filename)


def _setup_vertical_panels(number_of_panels):
    figure, axes = plt.subplots(number_of_panels, gridspec_kw={'hspace':0})
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


def raman_overtones(series, interval, scalex, image_filename):
    max_x = np.max(series.x)
    number_of_panels = int(np.ceil(max_x/interval[1]))
    print(number_of_panels)
    figure, axes = _setup_vertical_panels(number_of_panels)
    figure.subplots_adjust(hspace=0)
    plt.setp([a.get_xticklabels() for a in figure.axes[:-1]], visible=False)
    for i in range(number_of_panels): # start top and go down
        min, max = interval
        min += interval[1]*i
        max += interval[1]*i
        axis_number = number_of_panels - i - 1
        axes[axis_number].set_xlim([min, max])
        single_series_plot(axes[axis_number], series, scalex)
        #axes[axis_number].set_yticks([])
    plt.xlabel('Raman shift [$cm^{-1}$]')
    set_shared_ylabel(figure, axes, 'Intensity [A.U]')
    return (figure, axes, image_filename)
