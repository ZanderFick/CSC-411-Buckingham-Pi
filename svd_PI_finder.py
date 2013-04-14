import scipy as sp
import numpy
from scipy.linalg import svd

def svd_buck(input_matrix, eps=1e-15):
    inshape = input_matrix.shape
    padded_input_matrix = numpy.zeros([max(inshape)]*2)
    padded_input_matrix[:inshape[0], :inshape[1]] = input_matrix
    U, S, Vh = svd(padded_input_matrix.T)
    null_space = Vh[S <= eps, :]
    # make integer
    null_space = null_space/numpy.ma.masked_equal(numpy.abs(null_space), 0).min(0)
    return null_space.T
