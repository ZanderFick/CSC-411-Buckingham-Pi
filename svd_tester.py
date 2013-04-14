import unittest
import numpy
import svd_PI_finder

class TestKnownValues(unittest.TestCase):

    def test_pressure_drop(self):  
        a = numpy.array([[-3, 0, 1],
                         [-1, -2, 1],
                         [-1, -1, 1],
                         [1, -1, 0],
                         [1, 0, 0],
                         [1, 0, 0]])  
                         
        svd_PI_finder.buck(a) 
 
        
if __name__ == '__main__':
    unittest.main()