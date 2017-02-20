from plots import dos_bands
import matplotlib.pyplot as plt


def crystal14_bands(paths):
    print('received paths ', paths)

def crystal14_dos(path):
    print('received path ', path)

import runpy

script_globals = runpy.run_path('/home/davide/avatar/plots/phep/crystal/dos-bands/d4h-large/plot.py', init_globals={'dos_bands': dos_bands, 'crystal14_bands': crystal14_bands, 'crystal14_dos': crystal14_dos})


