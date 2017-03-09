from thesisplots.readers import crystal14_bands
import os


def test_crystal():
    paths = [{'ticks': ['A', 'B'], 'file': 'readers'}]
    dataroot = '/home/davide/progetti/thesisplots/thesisplots/tests'
    tutto = crystal14_bands(paths, dataroot)
    print(tutto)


if __name__ == '__main__':
    test_crystal()