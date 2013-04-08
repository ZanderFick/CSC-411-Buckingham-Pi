import unittest
import numpy
import svd_PI_finder

class TestKnownValues(unittest.TestCase):
    def test_ones(self):
        a = numpy.array([[1, 1],
                         [1, 1]])
        print svd_PI_finder.svd_buck(a) 


    def test_strange(self):
        a = numpy.array([[1, 0, 0],
                         [1, 1, 1],
                         [0, 1, 1]])
        print svd_PI_finder.svd_buck(a)

    def test_pendulum(self):
        a = numpy.array([[-2, 0, 1],
                         [0, 0, 1],
                         [0, 1, 0],
                         [1, 0, 0]])
        print svd_PI_finder.svd_buck(a)    

    def test_speed(self):
        a = numpy.array([[1, 0],
                         [0, 1],
                         [1, -1]])
        print svd_PI_finder.svd_buck(a) 
        
    def test_pendulum(self):
        a = numpy.array([[1, 0, 0, -2],
                         [0, 1, 0, 0],
                         [0, 0, 1, 1]]).T
        print svd_PI_finder.svd_buck(a) 

    def test_reynolds(self):
        a = numpy.array([[-3, 0, 1],
                         [1, -1, 0],
                         [1, 0, 0],
                         [-1, -1, 1]])
        print svd_PI_finder.svd_buck(a) 

    def test_archimedes(self):
        a = numpy.array([[-3, 0, 1],
                         [1, 0, 0],
                         [1, -2, 0],
                         [-1, -1, 1]])
        print svd_PI_finder.svd_buck(a) 

    def test_pressure_drop(self):  
        a = numpy.array([[-3, 0, 1],
                         [-1, -2, 1],
                         [-1, -1, 1],
                         [1, -1, 0],
                         [1, 0, 0],
                         [1, 0, 0]])  
                         
        print svd_PI_finder.svd_buck(a) 
 
        
if __name__ == '__main__':
    unittest.main()