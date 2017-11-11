from __future__ import absolute_import

from typing import List, Type

import matplotlib.pyplot as plt

from thesisplots.crystallography import (bands_2_dos, dos_bands, dos_only,
                                         dos_only_correct, huckel_and_crystal)
from thesisplots.spectroscopy import (ir_compare, raman, raman_compare,
                                      raman_overtones, raman_compare_overlapped)
from thesisplots.generic import compare_bond_length
from thesisplots.tools import *

# TODO non dovrebbe essere necessario indicare le funzioni
