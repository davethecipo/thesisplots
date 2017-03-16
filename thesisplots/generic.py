from __future__ import absolute_import

from typing import List, Type
from matplotlib import gridspec
import matplotlib.pyplot as plt

from thesisplots.tools import Series

def _setup_bond_length():
    figure = plt.figure()
    gs = gridspec.GridSpec(1, 1)
    ax = plt.subplot(gs[0])
    ax.set_ylabel('Bond length [\AA]')
    ax.set_xlabel('Bond number')
    return figure, ax


def compare_bond_length(series: List[Series], image_filename: str):
    fig, ax = _setup_bond_length()
    for data in series:
        ax.plot(data.x, data.y, label=data.legend)
    return (fig, ax, image_filename)