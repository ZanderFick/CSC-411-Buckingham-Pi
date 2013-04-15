import numpy
import fractions
from scipy.linalg import svd

def buck(input_matrix, eps=1e-16):
    
    inshape = input_matrix.shape
    [c,r] = inshape
    if c < r:
        padded_input_matrix = numpy.zeros([max(inshape)]*2)
        padded_input_matrix[:inshape[0], :inshape[1]] = input_matrix
        U, S, Vh = svd(padded_input_matrix.T)
        null_space = Vh[S <= eps, :]
        print "padded input_mat" , padded_input_matrix.T
    else:
        U, S, Vh = svd(input_matrix.T)
        null_space = Vh[S <= eps, :]
        print "non padded input_mat" , input_matrix.T
        
 
# make integer
    
    print "null_space", null_space.T  
    return null_space.T
