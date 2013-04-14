import numpy
import fractions
from scipy.linalg import svd
from pandas import *

def buck(input_matrix, eps=1e-16):
#Delete null rows
    
    
    inshape = input_matrix.shape
    padded_input_matrix = numpy.zeros([max(inshape)]*2)

    padded_input_matrix[:inshape[0], :inshape[1]] = input_matrix

    U, S, Vh = svd(padded_input_matrix.T)
    null_space = numpy.matrix(Vh[S <= eps, :])
    
# make integer
    
    [rows, cols] = null_space.shape
    result = numpy.zeros(null_space.shape)
    for r in range(0,rows):
        pi_group = numpy.array(null_space[r,:])
        numer = numpy.zeros(pi_group.shape)
        denom = numpy.zeros(pi_group.shape)
        for c in range(0,cols):
            fraction = fractions.Fraction(str(pi_group[0,c])).limit_denominator(25)
            a = fraction.numerator
            b = fraction.denominator
            numer[0,c] = a
            denom[0,c] = b
        numer = 
        print numer
        print denom

    
    return null_space.T
