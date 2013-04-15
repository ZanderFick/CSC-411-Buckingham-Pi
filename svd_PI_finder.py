import numpy
import fractions
from scipy.linalg import svd

def buck(input_matrix, eps=1e-16):
    inshape = input_matrix.shape
    padded_input_matrix = numpy.zeros([max(inshape)]*2)
    padded_input_matrix[:inshape[0], :inshape[1]] = input_matrix
    U, S, Vh = svd(padded_input_matrix.T)
    null_space = Vh[S <= eps, :]

# make integer
    null_space = numpy.round(null_space/numpy.ma.masked_less(numpy.abs(null_space.T), 1e-10).min(0).T) 
    return null_space.T
