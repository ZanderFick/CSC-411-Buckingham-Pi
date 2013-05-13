import numpy
from scipy.linalg import svd


def buck(input_matrix, eps=1e-14):

    inshape = input_matrix.shape

    if input_matrix.size > 1:
        if inshape[1] < inshape[0]:
            padded_input_matrix = numpy.zeros([max(inshape)]*2)
            padded_input_matrix[:inshape[0], :inshape[1]] = input_matrix

        else:
            padded_input_matrix = input_matrix
        U, S, Vh = svd(padded_input_matrix.T)
        null_space = Vh[S <= eps, :]

        [r, c] = null_space.shape
        mask = numpy.ma.masked_less(numpy.abs(null_space.T), 1e-10).min(0).T
        for r in range(0, r):
            null_space[r, :] = null_space[r, :]/mask[r]
            if numpy.min(null_space[r, :]) != 0:
                null_space[r, :] = null_space[r, :]/numpy.min(null_space[r, :])
            neg_test = 0
            for c in range(0, c):
                neg_test += null_space[r, c]/numpy.absolute(null_space[r, c])
            if neg_test < 0:
                 null_space[r, :] = null_space[r, :]/-1
        
        return null_space.T