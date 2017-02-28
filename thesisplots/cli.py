from __future__ import absolute_import

from argparse import ArgumentParser
import configparser
import itertools
import matplotlib
import matplotlib.pyplot as plt
import os
import sys
import types

from appdirs import AppDirs

from thesisplots import plots, readers
from thesisplots.thesisplots import draw_single_image
from thesisplots.__version__ import version

dirs = AppDirs("thesistools")
conf_dir = dirs.user_config_dir


def print_info():
    print('thplot version: ', version)
    print('Supported image formats:')
    for elem in list(plt.gcf().canvas.get_supported_filetypes().keys()):
        print("\t{}".format(elem))
    print('Available styles:')
    for elem in plt.style.available:
        print("\t{}".format(elem))
    stylefolder = os.path.join(matplotlib.get_configdir(), 'stylelib')
    print('Stylesheet directory: {}/stylelib'.format(stylefolder))
    print('Config directory: {}'.format(conf_dir))


class Commands(object):
    # taken from
    # http://chase-seibert.github.io/blog/2014/03/21/python-multilevel-argparse.html
    def __init__(self):
        parser = ArgumentParser(
            description='Generate plots ',
            usage='''thplots <command> [<args>]

The available commands are:
   exec              Execute a particular script
   execall           Execute all scripts contained in a folder
   genbash           Generate a bash script that can run all plot scripts (one per line)
   info              Print information about the current configuration
''')
        parser.add_argument('command', help='Subcommand to run')
        # parse_args defaults to [1:] for args, but you need to
        # exclude the rest of the args too, or validation will fail
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print('Unrecognized command')
            parser.print_help()
            exit(1)
        # use dispatch pattern to invoke method with same name
        getattr(self, args.command)()

    def exec(self):
        parser = ArgumentParser(
            description='Run a single script')
        # now that we're inside a subcommand, ignore the first
        # TWO argvs, ie the command and the subcommand
        parser.add_argument('script', help='A thplot script')
        parser.add_argument('dataroot', help='Root folder where the data is stored')
        parser.add_argument('--styles', help='Plot using these styles, overriding the config file')
        args = parser.parse_args(sys.argv[2:])

        paths = {'dataroot': args.dataroot}

        for key, value in paths.items():
            if not os.path.isabs(value):
                cwd = os.getcwd()
                path = os.path.join(cwd, value)
                paths[key] = path

        all_plot_functions = [plots.__dict__.get(a) for a in dir(plots)
                              if isinstance(plots.__dict__.get(a), types.FunctionType) and not a.startswith('_')]

        all_reader_functions = [readers.__dict__.get(a) for a in dir(readers)
                                if isinstance(readers.__dict__.get(a), types.FunctionType) and not a.startswith('_')]

        config = configparser.ConfigParser()
        config.read(os.path.join(conf_dir, 'config.ini'))

        def comma_separated_options(section, option):
            return [e.strip() for e in config.get(section, option).split(',')]

        styles = comma_separated_options('Styling', 'styles')
        # TODO override if cli options is not empty
        img_formats = comma_separated_options('Formats', 'extensions')

        combinations = list(itertools.product(styles, img_formats))

        # TODO profiling per vedere se si può parallelizzare
        for (style, extension) in combinations:
            draw_single_image(style, extension, args.script, paths['dataroot'], all_plot_functions, all_reader_functions)

    def execall(self):
        parser = ArgumentParser(
            description='Run all scripts contained in a folder')
        parser.add_argument('scriptroot', help='Folder that contains all the thplot scripts')
        parser.add_argument('dataroot', help='Root folder where the data is stored')
        parser.add_argument('--styles', help='Plot using these styles, overriding the config file')
        args = parser.parse_args(sys.argv[2:])

        paths = {'dataroot': args.dataroot, 'scriptroot': args.scriptroot}

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

        print('reader functions DDDDDDDDDDDDDDDDDDDDDD, ', all_reader_functions)

        config = configparser.ConfigParser()
        config.read(os.path.join(conf_dir, 'config.ini'))

        def comma_separated_options(section, option):
            return [e.strip() for e in config.get(section, option).split(',')]

        styles = comma_separated_options('Styling', 'styles')
        # TODO override if cli options is not empty
        img_formats = comma_separated_options('Formats', 'extensions')

        all_scripts = []
        for root, subdirs, files in os.walk(paths['scriptroot']):
            pys = [f for f in files if f.endswith('py')]
            if len(pys) != 0:
                for elem in pys:
                    all_scripts.append(os.path.join(root, elem))

        combinations = list(itertools.product(styles, all_scripts, img_formats))

        # TODO profiling per vedere se si può parallelizzare
        for (style, script, extension) in combinations:
            draw_single_image(style, extension, script, paths['dataroot'], all_plot_functions, all_reader_functions)

    def genbash(self):
        parser = ArgumentParser(
            description='Generate a bash script that can run all plot scripts (one per line)')
        parser.add_argument('scriptroot', help='Folder that contains all the thplot scripts; bash file saved here')
        parser.add_argument('dataroot', help='Root folder where the data is stored')
        parser.add_argument('--styles', help='Plot using these styles, overriding the config file')
        args = parser.parse_args(sys.argv[2:])
        print(args)

    def info(self):
        parser = ArgumentParser(
            description="Obtain information about the current configuration")
        print_info()


def run_script():
    pass

def main():
    parser = Commands()



if __name__ == '__main__':
    main()