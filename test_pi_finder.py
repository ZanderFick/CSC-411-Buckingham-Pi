#!/usr/bin/env python

import unittest
import numpy
import PI_Finder

class TestKnownValues(unittest.TestCase):
    def test_ones(self):
        a = numpy.array([[1, 1],
                         [1, 1]])
        calculated = PI_Finder.buck(a)
        expected = numpy.array([[1],
                                [-1]])
        numpy.testing.assert_almost_equal(calculated, expected)
        

    def test_strange(self):
        a = numpy.array([[1, 0, 0],
                         [1, 1, 1],
                         [0, 1, 1]])
        calculated = PI_Finder.buck(a)
        expected = numpy.array([[-1],
                                [1],
                                [-1]])
        numpy.testing.assert_almost_equal(calculated, expected)


if __name__ == '__main__':
    unittest.main()
