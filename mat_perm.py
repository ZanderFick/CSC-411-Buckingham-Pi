import numpy as np
import itertools

from pandas import *

from itertools import *
from numpy import *
p = 4



d = np.zeros([1,p])

for c1 in range(0, p+1): 
    
    c2 = p-c1
    iter_mat = concatenate((np.ones([c1]), np.zeros([c2])), 0)

    for z in itertools.permutations(iter_mat, p):
        intermediate = np.asmatrix(z)
        d = np.concatenate((d, np.asmatrix(z)), 0)
r = DataFrame(d).drop_duplicates().values

print r
