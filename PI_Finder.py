import numpy as np
import itertools

from pandas import *
from itertools import *
from numpy import *


def perm_set(a):
    if a == 0:
        return []
    elif a == 1:
        return np.array([[0], [1]])
    elif a > 1:
        
        d = np.zeros([a, a*a])
        
        for c1 in range(0,a):
            n_ones = a + c1
            ones_interv = np.floor(a*a/n_ones) +1
            for c2 in range(0,a*a):
                if np.mod(c2,ones_interv) == 0 and n_ones > 0:
                    d[c1,c2] = 1
                    n_ones += -1                
        
    return d


def buck(input_matrix):
    [rows, cols] = input_matrix.shape

    iszero = 1
    for rowc in range(0, rows):
        row = rows - rowc - 1
        for col in range(0, cols):
            if input_matrix[row, col] != 0:
                iszero = 0
        if iszero == 1:
            input_matrix = np.delete(input_matrix, (row), axis=0)

    [rows, cols] = input_matrix.shape

    D_mat = input_matrix.T
#Delete null rows
    D_mat = D_mat[D_mat.any(1)]

#get matrix dimensions
    [d, k] = D_mat.shape

    p = k-d
    if p < 0:
        print ""
    #Is the handling of systems with more dimensions than variables feasable
    #when taking into account the function of this project?
    elif d >= 1 and k >= 1:
#Create righthand A-matrix and remove singularities
        A_det = 0

        while A_det == 0:
            A_mat = D_mat.T[p:k].T
            A_det = np.linalg.det(A_mat)
            A_rank = np.linalg.matrix_rank(A_mat)
            delta = d - A_rank

            if delta == 0 and A_det == 0:
#randomly swap two columns
                r = random.randint(0, k-1)
                D_mat[:, [0, 1+r]] = D_mat[:, [1+r, 0]]

            elif A_det == 0 and delta != 0:
#remove singular rows and create new dimensional matrix
                u, s, v = np.linalg.svd(A_mat)
                D_mat = D_mat[s > 1e-10]
                [d, k] = D_mat.shape
                p = k-d

#Create lefthand B-matrix
        B_mat = D_mat.T[0:p].T

#Create the E I matrix
        I_mat = np.identity(p)

#Create the E null patrix

        null_mat = np.zeros([p, d])

#Create the -inv(A)B submatrix

        A_inv = np.linalg.inv(A_mat)

        invAB_mat = dot(A_inv, B_mat)*-1
#Assemble the E matrix

        E_mat_top = np.concatenate((I_mat, null_mat), axis=1)
        E_mat_bottom = np.concatenate((invAB_mat, A_inv), axis=1)

        E_mat = np.concatenate((E_mat_top, E_mat_bottom), axis=0)

#Set up the Z matrix
#Added advantage that other groups (not non-dimensional) can be found
#simply by seting the last k rows to the desired type of dimensional group
#power values For the non dimensional case they are simply set to zero

#create the q sub matrix for the non dimensional case

        q_mat = np.zeros([d, p])

#create the remaining non singular top Z sub matrix
        top_mat_perm = perm_set(p)

        [p_row, p_col] = top_mat_perm.shape

# create the result matrix
        Pi_result = np.zeros([rows, 0])

        for rescount in range(p_row):
            t_vect = np.asmatrix(top_mat_perm[rescount])
            if p_row > 2:
                top_mat = np.concatenate((t_vect[0, :p], t_vect[0, -p:]), 0)

            else:
                top_mat = t_vect

            Z_mat = np.concatenate((top_mat, q_mat), axis=0)

#the resulting P matrix columns represent the pi groups

            Pi_mat = around((dot(E_mat, Z_mat)), decimals=2)

            Pi_result = np.concatenate((Pi_result, Pi_mat), 1)

            Pi_result = Pi_result.T[Pi_result.T.any(1)].T

        return DataFrame(Pi_result.T).drop_duplicates().values.T