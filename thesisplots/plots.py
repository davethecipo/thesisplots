from __future__ import absolute_import

from typing import List, Type

import matplotlib.pyplot as plt

from thesisplots.crystallography import (bands_2_dos, dos_bands, dos_only,
                                         dos_only_correct)
from thesisplots.spectroscopy import (ir_compare, raman, raman_compare,
                                      raman_overtones)
from thesisplots.tools import Series

# TODO non dovrebbe essere necessario indicare le funzioni
