from __future__ import absolute_import

import os
from collections import namedtuple
from functools import wraps
from typing import List, Type

import numpy as np

Series = namedtuple('Series', ['x', 'y', 'legend', 'opts'], verbose=False)


def normalize(vec):
    maximum = np.max(vec)
    return np.array([elem / maximum for elem in vec])


def shift_up(data, how_much):
    return np.array([elem + how_much for elem in data])


def compare_and_shift(setup_function, single_function, series: List[Type[Series]]):
    figure, axis = setup_function()
    offset = 0
    for i, elem in enumerate(series):
        intensity = shift_up(normalize(elem.y), offset)
        normalized_elem = Series(elem.x, intensity, elem.legend, opts=elem.opts)
        offset += 1
        single_function(axis, normalized_elem)
    axis.set_ylim([-0.02, offset*1.02])
    axis.set_yticklabels([])
    return figure, axis


def save_no_legend(information):
    (fig, axis, file) = information
    fig.savefig(file, bbox_inches='tight')


def save_with_legend(information):
    (fig, axis, file) = information
    # Shrink current axis by 20%, let space for legend on the right
    box = axis.get_position()
    axis.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    handles, labels = axis.get_legend_handles_labels()
    legend = axis.legend(handles[::-1], labels[::-1], loc='center left', bbox_to_anchor=(1, 0.5))
    fig.savefig(file, bbox_extra_artists=(legend,), bbox_inches='tight')


def modify_filename(function, basedir, name_prefix: str, extension: str):
    @wraps(function)
    def inner(*args, **kwargs):
        name_arg = kwargs['image_filename']  # the value of the dict element gets copied to a new variable
        name_arg = "{}-{}.{}".format(name_prefix, name_arg, extension)
        name_arg = os.path.join(basedir, name_arg)
        kwargs['image_filename'] = name_arg  # put the new value back into the dict
        return function(*args, **kwargs)

    return inner


def apply_dataroot(function, dataroot):
    @wraps(function)
    def inner(*args, **kwargs):
        return function(*args, **kwargs, dataroot=dataroot)
    return inner


def single_series_plot(axis, shift: Type[Series], scalex=1):
    axis.plot(shift.x*scalex, shift.y, label=shift.legend, **shift.opts)
