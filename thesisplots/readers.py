from __future__ import absolute_import

import logging
import os
import sys

import numpy as np
from matplotlib.pyplot import imshow, pause, plot
import ipdb


from thesisplots.tools import Series

logger = logging.getLogger(__name__)


def column_bands(paths, dataroot, opts=None):
    if opts is None:
        opts = {} # ugly stuff, but allows setting particular options from scripts
    global_lines = []
    x_offset = 0
    x_tick_labels = []
    x_tick_positions = []
    mapazzoni = []
    #ipdb.set_trace()
    for i, elem in enumerate(paths):
        path = elem['file']
        band_file = os.path.join(dataroot, path)
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
            x_tick_positions.append(0)
            x_offset += len(mapazzone[:,0])-1
            x_tick_positions.append(x_offset)
        if i!=0:
            x_offset += len(mapazzone[:,0]) -1
            tick_list = paths[i]['ticks']
            # follwing paths: specify only the last xtick label
            if len(tick_list) != 1:
                logger.error('You should specify one k-point label for all the segments but the first, exiting')
                sys.exit(1)
            x_tick_labels.append(*tick_list)
            x_tick_positions.append(x_offset)
    total = np.vstack(mapazzoni)
    bands_number = len(total[0, :])
    length = len(total[:, 0])
    x = np.array(list(range(length)))
    for band in range(0, bands_number):
        data = Series(x, total[:, band], legend=band, opts=opts)
        global_lines.append(data)
    return global_lines, x_tick_labels, x_tick_positions



def crystal14_bands(paths, dataroot, opts=None):
    if opts is None:
        opts = {} # ugly stuff, but allows setting particular options from scripts
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

    #pdb.set_trace()

    previous_length = 0
    for i, mapazzone in enumerate(mapazzoni):
        
        if i==0: # don't add offset for the first
            # first path: specify both extreme xticks labels
            should_be_both_ticks = paths[i]['ticks']
            if len(should_be_both_ticks) != 2:
                logger.error('You should specify two k-points labels for the first segment, exiting')
                sys.exit(1)
            x_tick_labels.append(should_be_both_ticks[0])
            x_tick_labels.append(should_be_both_ticks[1])
            x_tick_positions.append(0)
        if i!=0:
            x_offset = mapazzoni[i-1][-1, 0]
            mapazzone[:, 0] += x_offset
            tick_list = paths[i]['ticks']
            # follwing paths: specify only the last xtick label
            if len(tick_list) != 1:
                logger.error('You should specify one k-point label for all the segments but the first, exiting')
                sys.exit(1)
            x_tick_labels.append(*tick_list)
        previous_length += len(mapazzone[:, 0])
        ipdb.set_trace()
        x_tick_positions.append(previous_length)
    total = np.vstack(mapazzoni)
    bands_number = len(total[0,1:])
    #print(bands_number)
    length = len(total[:, 0])
    x = np.array(list(range(length)))
    for band in range(1, bands_number+1):
        data = Series(x, total[:, band], legend=band, opts=opts)
        global_lines.append(data)
    return global_lines, x_tick_labels, x_tick_positions


def crystal14_dos(path, column, dataroot):
    fpath = os.path.join(dataroot, path, 'DOSS.DAT')
    y, x = np.loadtxt(fpath, unpack=True, comments=['#', '@'], usecols=[0, column-1])
    return Series(x, y, legend=None, opts=None)



def crystal_raman(path, dataroot, scale_freq=0.98, legend=None, opts=None):
    if opts is None:
        opts = {}
    fname = os.path.join(dataroot, path, 'vib/rplots/raman.dat')
    x, y = np.loadtxt(fname, unpack=True)
    return Series(x*scale_freq, y, legend=legend, opts=opts)


def iraman(path, dataroot,  scale_freq=0.98, legend=None, opts=None):
    if opts is None:
        opts = {}
    fname = os.path.join(dataroot, path)
    x, y = np.loadtxt(fname, unpack=True)
    return Series(x*scale_freq, y, legend=legend, opts=opts)

# TODO rename to more general (e.g I use it also for bond length data)
def expraman(filepath, dataroot, columns, legend=None, opts=None):
    """start counting columns from 1"""
    if opts is None:
        opts = {}
    complete_path = os.path.join(dataroot, filepath)
    x, y = np.loadtxt(complete_path, unpack=True, usecols=[col-1 for col in columns])
    return Series(x, y, legend=legend, opts=opts)