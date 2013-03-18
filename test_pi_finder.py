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
        expected = numpy.array([[1],
                                [-1],
                                [1]])
        numpy.testing.assert_almost_equal(calculated, expected)

    def test_speed(self):
        a = numpy.array([[1, 0],
                         [0, 1],
                         [1, -1]])
        calculated = PI_Finder.buck(a)
        expected = numpy.array([[1],
                                [-1],
                                [-1]])
        numpy.testing.assert_almost_equal(calculated, expected)

    def test_pendulum(self):
        a = numpy.array([[1, 0, 0, -2],
                         [0, 1, 0, 0],
                         [0, 0, 1, 1]]).T
        calculated = PI_Finder.buck(a)
        expected = numpy.array([[1],
                                [0],
                                [-0.5],
                                [0.5]])
        numpy.testing.assert_almost_equal(calculated, expected)

    def test_reynolds(self):
        a = numpy.array([[-3, 0, 1],
                         [1, -1, 0],
                         [1, 0, 0],
                         [-1, -1, 1]])
        calculated = PI_Finder.buck(a)
        expected = numpy.array([[1],
                                [1],
                                [1],
                                [-1]])
        numpy.testing.assert_almost_equal(calculated, expected)

    def test_archimedes(self):
        a = numpy.array([[-3, 0, 1],
                         [1, 0, 0],
                         [1, -2, 0],
                         [-1, -1, 1]])
        calculated = PI_Finder.buck(a)
        expected = numpy.array([[1],
                                [1.5],
                                [0.5],
                                [-1]])
        numpy.testing.assert_almost_equal(calculated, expected)


if __name__ == '__main__':
    unittest.main()