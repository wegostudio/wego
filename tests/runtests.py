import unittest
import os
import sys

path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.dirname(path))


def test_all():
    dir_list = [f for f in os.listdir(path) if not os.path.isfile(os.path.join(path, f))]
    modules = [__import__('{}.tests'.format(d)).tests for d in dir_list]
    load = unittest.defaultTestLoader.loadTestsFromModule
    return unittest.TestSuite(map(load, modules))

unittest.main(defaultTest='test_all')
