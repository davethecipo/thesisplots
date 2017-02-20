from argparse import ArgumentParser
import matplotlib.pyplot as plt
import os
import runpy
import types

from thesisplots import plots, readers
from thesisplots.tools import modify_filename

import ipdb

parser = ArgumentParser()
parser.add_argument('dataroot', help='Root folder where the data is stored')
parser.add_argument('plotroot', help='Root folder where plot scripts are stored')
args = parser.parse_args()

paths = {'dataroot': args.dataroot, 'plotroot': args.plotroot}

# ensure paths are absolute
for key, value in paths.items():
    if not os.path.isabs(value):
        cwd = os.getcwd()
        path = os.path.join(cwd, value)
        paths[key] = path






all_plot_functions = [plots.__dict__.get(a) for a in dir(plots)
                      if isinstance(plots.__dict__.get(a), types.FunctionType) and not a.startswith('_')]

all_reader_functions = [readers.__dict__.get(a) for a in dir(readers)
                      if isinstance(readers.__dict__.get(a), types.FunctionType) and not a.startswith('_')]




# da parallelizzare
def draw_single_image(style, extension, plot_script):
    script_folder = os.path.dirname(plot_script)
    def decorate_all_plot_functions(prefix, extension):
        decorated = []
        for function in all_plot_functions:
            decorated.append(modify_filename(function, script_folder, prefix, extension))
        return decorated
    plt.style.use(style)
    decorated = decorate_all_plot_functions(style, extension)
    decorated_globals = {f.__name__: f for f in decorated}
    decorated_globals.update({f.__name__: f for f in all_reader_functions})
    runpy.run_path(plot_script, init_globals=decorated_globals)



draw_single_image('ggplot', 'pdf', '/home/davide/proveplot.py')
draw_single_image('ggplot', 'png', '/home/davide/proveplot.py')


# for style in styles:
# draw()
