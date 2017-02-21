from typing import List, Type
from matplotlib import gridspec
import matplotlib.pyplot as plt

from thesisplots.tools import Series

def _setup_dos_bands():
    figure = plt.figure()
    gs = gridspec.GridSpec(1, 2, width_ratios=[3, 1])
    bands_ax, dos_ax = plt.subplot(gs[0]), plt.subplot(gs[1])
    bands_ax.set_ylabel('Energy [Hartree]')
    bands_ax.set_title('Band structure')
    bands_ax.set_xticks([])
    return figure, [bands_ax, dos_ax]


def dos_bands(bands_bundle, dos: Type[Series], image_filename: str):
    bands_segment, x_tick_labels, x_tick_positions = bands_bundle
    print('dentro dos bands non decorata')
    figure, axes = _setup_dos_bands()
    [band_axis, dos_axis] = axes
    band_axis.set_xlim([bands_segment[0].x[0], bands_segment[0].x[-1]])
    for band in bands_segment:
        band_axis.plot(band.x, band.y, label=band.legend, *band.opts)
    band_axis.set_xticks(x_tick_positions)
    band_axis.set_xticklabels(x_tick_labels)
    print('FFFFFFFFFFFFFFFFFFF function dos_bands receives file variable', image_filename)
    return (figure, axes, image_filename)