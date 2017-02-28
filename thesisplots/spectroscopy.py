from __future__ import absolute_import

import matplotlib.pyplot as plt
from typing import List, Type

from thesisplots.tools import single_series_plot
from thesisplots.tools import Series, compare_and_shift


def _setup_raman():
    figure, axis = plt.subplots(1, 1)
    axis.set_xlabel('Raman shift [$cm^{-1}$]')
    return figure, axis


def _setup_ir():
    figure, axis = plt.subplots(1, 1)
    axis.set_xlabel('Absorbance [A.U]')
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
