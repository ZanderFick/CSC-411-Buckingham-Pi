import scipy as sp
from scipy.linalg import svd


def svd_buck(input_matrix):

    U, S, V = svd(input_matrix.T)
    zero_close = 1e-15
    S_mask = (S <= zero_close)
    null_space = sp.compress(S_mask, V, axis=0)

    return (sp.transpose(null_space))
