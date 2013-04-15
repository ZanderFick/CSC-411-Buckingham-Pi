import unittest
import numpy
import svd_PI_finder

class TestKnownValues(unittest.TestCase):
    def test_ones(self):
        a = numpy.array([[1, 1, 1],
                         [1, 1, 1]])
        print svd_PI_finder.buck(a) 

 
        
if __name__ == '__main__':
    unittest.main()