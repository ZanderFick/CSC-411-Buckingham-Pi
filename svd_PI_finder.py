import numpy
import fractions
from scipy.linalg import svd
from pandas import *

def buck(input_matrix, eps=1e-16):
#Delete null rows
    input_matrix = input_matrix.T
    input_matrix = input_matrix[input_matrix.any(1)].T
    
    inshape = input_matrix.shape
    padded_input_matrix = numpy.zeros([max(inshape)]*2)

    padded_input_matrix[:inshape[0], :inshape[1]] = input_matrix

    U, S, Vh = svd(padded_input_matrix.T)
    null_space = numpy.matrix(Vh[S <= eps, :])
    
# make integer
    
    null_space = numpy.round(null_space/numpy.ma.masked_equal(numpy.abs(null_space.T), 0).min(0).T)
    print null_space.T
    
    return null_space.T
