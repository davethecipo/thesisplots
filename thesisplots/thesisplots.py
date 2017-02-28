from __future__ import absolute_import

import matplotlib.pyplot as plt
import os
import runpy
from typing import List, Callable

from thesisplots.tools import modify_filename, apply_dataroot, save_with_legend, save_no_legend


def draw_single_image(
        style: str,
        ext: str,
        plot_script: str,
        dataroot: str,
        plt_functs: List[Callable],
        read_functs: List[Callable]):

    script_folder = os.path.dirname(plot_script)
    def decorate_all_plot_functions(prefix, extension):
        decorated = []
        for function in plt_functs:
            decorated.append(modify_filename(function, script_folder, prefix, extension))
        return decorated
    def decorate_all_reader_functs(functions):
        applied = []
        for f in functions:
            applied.append(apply_dataroot(f, dataroot))
        return applied
    plt.style.use(style)
    decorated_plots = decorate_all_plot_functions(style, ext)
    decorated_plot_globals = {f.__name__: f for f in decorated_plots}
    decorated_readers = decorate_all_reader_functs(read_functs)
    decorated_reader_globals = {f.__name__: f for f in decorated_readers}
    decorated_plot_globals.update(decorated_reader_globals)
    decorated_plot_globals.update({'save_with_legend': save_with_legend, 'save_no_legend': save_no_legend })
    runpy.run_path(plot_script, init_globals=decorated_plot_globals)
    #(figure, axes, image_filename) = script_globals['img']



