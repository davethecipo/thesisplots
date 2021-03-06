from __future__ import absolute_import

from typing import List, Type
from matplotlib import gridspec
import matplotlib.pyplot as plt

from thesisplots.tools import Series

def _setup_dos():
    figure = plt.figure(figsize=(4, 5))
    gs = gridspec.GridSpec(1, 1)
    bands_ax = plt.subplot(gs[0])
    bands_ax.set_ylabel('Energy [Hartree]')
    bands_ax.set_title('Band structure')

    bands_ax.set_xticks([])

    return figure, bands_ax

def _setup_dos_bands():
    figure = plt.figure()
    gs = gridspec.GridSpec(1, 2, width_ratios=[3, 3])
    bands_ax, dos_ax = plt.subplot(gs[0]), plt.subplot(gs[1])
    bands_ax.set_ylabel('Energy [Hartree]')
    bands_ax.set_title('Band structure')
    dos_ax.set_title('D.O.S')
    bands_ax.set_xticks([])
    dos_ax.set_xticks([])
    dos_ax.set_yticks([])
    return figure, [bands_ax, dos_ax]


def _setup_2_dos_bands():
    figure = plt.figure()
    gs = gridspec.GridSpec(1, 3, width_ratios=[3, 2, 2])
    bands_ax, dos1_ax, dos2_ax = [plt.subplot(gs[0]), plt.subplot(gs[1]), plt.subplot(gs[2])]
    bands_ax.set_ylabel('Energy [Hartree]')
    bands_ax.set_title('Band structure')
    dos1_ax.set_title('D.O.S')
    dos2_ax.set_title('D.O.S')
    bands_ax.set_xticks([])
    dos1_ax.set_xticks([])
    dos2_ax.set_xticks([])
    dos1_ax.set_yticks([])
    dos2_ax.set_yticks([])

    return figure, [bands_ax, dos1_ax, dos2_ax]


def dos_bands(bands_bundle, dos: Type[Series], e_fermi, image_filename: str):
    bands, x_tick_labels, x_tick_positions = bands_bundle

    figure, axes = _setup_dos_bands()
    [band_axis, dos_axis] = axes
    band_axis.set_xlim([bands[0].x[0], bands[0].x[-1]])
    for band in bands:
        band_axis.plot(band.x, band.y+e_fermi, label=band.legend, color='black', linestyle='-')
    band_axis.set_xticks(x_tick_positions)
    band_axis.set_xticklabels(x_tick_labels)

    dos_axis.plot(dos.x, dos.y, color='black')
    band_axis.axhline(e_fermi, ls='-.', color='black')
    dos_axis.axhline(e_fermi, ls='-.', color='black')

    return (figure, axes, image_filename)


def bands_2_dos(bands_bundle, dos1, dos2, e_fermi, image_filename):
    bands, x_tick_labels, x_tick_positions = bands_bundle

    figure, axes = _setup_2_dos_bands()
    [band_axis, dos1_axis, dos2_axis] = axes
    band_axis.set_xlim([bands[0].x[0], bands[0].x[-1]])
    for band in bands:
        band_axis.plot(band.x, band.y+e_fermi, color='black', linestyle='-')
    band_axis.set_xticks(x_tick_positions)
    band_axis.set_xticklabels(x_tick_labels)

    dos1_axis.plot(dos1.x, dos1.y, color='black')
    dos2_axis.plot(dos2.x, dos2.y, color='black')

    band_axis.axhline(e_fermi, ls='-.', color='black')
    dos1_axis.axhline(e_fermi, ls='-.', color='black')
    dos2_axis.axhline(e_fermi, ls='-.', color='black')

    return (figure, axes, image_filename)


# TODO è sbagliato fare qua la traslazione, è un errore di crystal da correggere prima del plot
def dos_only(bands_bundle, e_fermi, image_filename: str):
    bands, x_tick_labels, x_tick_positions = bands_bundle

    figure, axes = _setup_dos()
    band_axis = axes
    band_axis.set_xlim([bands[0].x[0], bands[0].x[-1]])
    for band in bands:
        band_axis.plot(band.x, band.y+e_fermi, label=band.legend, color='black', linestyle='-')
    band_axis.set_xticks(x_tick_positions)
    band_axis.set_xticklabels(x_tick_labels)
    band_axis.axhline(e_fermi, ls='-.', color='black')
    return (figure, axes, image_filename)


def dos_only_correct(bands_bundle, e_fermi, image_filename: str):
    bands, x_tick_labels, x_tick_positions = bands_bundle

    figure, axes = _setup_dos()
    band_axis = axes
    band_axis.set_xlim([bands[0].x[0], bands[0].x[-1]])
    for band in bands:
        band_axis.plot(band.x, band.y, label=band.legend, color='black', linestyle='-')
    band_axis.set_xticks(x_tick_positions)
    band_axis.set_xticklabels(x_tick_labels)
    band_axis.axhline(e_fermi, ls='-.', color='black')
    return (figure, axes, image_filename)


def huckel_and_crystal(huckel_bands, crystal14_bundle, e_fermi, image_filename):
    crystal_bands, x_tick_labels, x_tick_positions = crystal14_bundle
    cry14_min = crystal_bands[0].x[0]
    cry14_max = crystal_bands[0].x[-1]

    # rescale ticks positions from 0 to 1
    x_tick_positions = x_tick_positions/cry14_max

    figure, axes = _setup_dos()
    band_axis = axes
    band_axis.set_xlim([0, 1])
    for band in crystal_bands:
        band_axis.plot(band.x/cry14_max, band.y, label='Crystal 14', linestyle='-', color='black', linewidth=0.4)
    
    import ipdb
    #ipdb.set_trace()
    huckel_min = huckel_bands[0].x[0]
    huckel_max = huckel_bands[0].x[-1]
    for band in huckel_bands:
        # rescale x
        band_axis.plot(band.x/huckel_max, band.y, label='Huckel', linestyle=':', color='red')
    band_axis.set_xticks(x_tick_positions)
    band_axis.set_xticklabels(x_tick_labels)
    band_axis.axhline(e_fermi, ls='-.', color='black')
    return (figure, axes, image_filename)
    