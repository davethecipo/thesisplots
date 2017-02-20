from typing import List, Type
import matplotlib.pyplot as plt

from thesisplots.tools import Series

def _setup_dos_bands():
    figure, axes = plt.subplots(1, 2, sharey=True)
    (bands_ax, dos_ax) = axes
    bands_ax.set_ylabel('Energy [Hartree]')
    bands_ax.set_title('Band structure')
    # also do the plotting, no saving
    return figure, axes


def dos_bands(band_structure: Type[Series], dos: Type[Series], file: str):
    figure, axes = _setup_dos_bands()
    # also do the plotting, no saving
    print('FILENAMEEEEEEEEEEEEEEEEEEEEEEEEE ', file)
    return (figure, axes, file)