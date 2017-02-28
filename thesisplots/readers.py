import logging
import os
import sys

import numpy as np
import ipdb

from thesisplots.tools import Series

logger = logging.getLogger(__name__)


def crystal14_bands(paths, dataroot, opts=None):
    if opts is None:
        opts = {} # ugly stuff, but allows setting particular options from scripts
    print('HELLLLOOOOOOOOO NURSE!')
    print(paths)
    global_lines = []
    x_offset = 0
    x_tick_labels = []
    x_tick_positions = []
    mapazzoni = []
    for i, elem in enumerate(paths):
        path = elem['file']
        band_file = os.path.join(dataroot, path, 'BAND.DAT')
        mapazzone = np.loadtxt(band_file, comments=['#', '@'])
        mapazzoni.append(mapazzone)
    for i, mapazzone in enumerate(mapazzoni):
        if i==0: # don't add offset for the first
            # first path: specify both extreme xticks labels
            should_be_both_ticks = paths[i]['ticks']
            if len(should_be_both_ticks) != 2:
                logger.error('You should specify two k-points labels for the first segment, exiting')
                sys.exit(1)
            x_tick_labels.append(should_be_both_ticks[0])
            x_tick_labels.append(should_be_both_ticks[1])
            x_tick_positions.append(mapazzone[0, 0])
            x_tick_positions.append(mapazzone[-1, 0])
        if i!=0:
            x_offset += mapazzoni[i-1][-1, 0]
            tick_list = paths[i]['ticks']
            # follwing paths: specify only the last xtick label
            if len(tick_list) != 1:
                logger.error('You should specify one k-point label for all the segments but the first, exiting')
                sys.exit(1)
            x_tick_labels.append(*tick_list)
            x_tick_positions.append(mapazzone[-1, 0]+x_offset)
        # each line is: k energy(1st band) energy(2nd band) energy(3rd band) energy(n-th bands)
        # repeat for each line
        for energy_band_index in range(1, len(mapazzone[0,:])):
            #ipdb.set_trace()
            # add the x offset element-wise to the first column, which contains the k values
            global_lines.append(Series(mapazzone[:, 0]+x_offset, mapazzone[:, energy_band_index], legend='', opts=opts))

    return global_lines, x_tick_labels, x_tick_positions

def crystal14_dos(path, dataroot):
    print('INSIDE DOOOOOOS')
    print('received path ', path)
    print('dataroot', dataroot)
    fpath = os.path.join(dataroot, path, 'DOSS.DAT')
    y, x = np.loadtxt(fpath, unpack=True, comments=['#', '@'])
    return Series(x, y, legend=None, opts=None)

def crystal_raman(path, dataroot, legend=None, opts=None):
    if opts is None:
        opts = {}
    fname = os.path.join(dataroot, path, 'vib/rplots/raman.dat')
    x, y = np.loadtxt(fname, unpack=True)
    return Series(x, y, legend=legend, opts=opts)


def iraman(path, dataroot, legend=None, opts=None):
    if opts is None:
        opts = {}
    fname = os.path.join(dataroot, path, 'spectra/iraman.dat')
    x, y = np.loadtxt(fname, unpack=True)
    return Series(x, y, legend=legend, opts=opts)


def expraman(filepath, dataroot, legend=None, opts=None):
    if opts is None:
        opts = {}
    complete_path = os.path.join(dataroot, filepath)
    x, y = np.loadtxt(complete_path, unpack=True)
    return Series(x, y, legend=legend, opts=opts)