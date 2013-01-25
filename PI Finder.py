import fractions
import numpy as np
import random

from scipy import linalg, matrix
from fractions import Fraction
from numpy import *

#def GCD(mat):
 #   A = abs(mat)
  #  [null , l] = A.shape
   # print A
   # if l >2:
    #    GCD(A[:,:-1])
    #elif l == 2:
     #   [[x,y]] = A
      #  if y ==0:
       #     return x
        #    print x
        #else:
         #   GCD(np.array([[y,np.remainder(x,y)]]))
        
#In this section the import from the GUI
#takes place whereby the dimensional matrix
#is set up and sent to this script

#For now the dimensional matrix is set up manually

#Consider the stirrer system:
    ## http://en.wikipedia.org/wiki/Dimensionless_number
#var's (Dh,mu,roh,P,n)

D_mat = np.array([[1, -1, -3, 2, 0],   #Length
                [0, -1, 0, -3, -1],        #Time
                [0, 1, 1, 1, 0],      #Mass                
                [0,0,0,0,0],        #Temperature
                [0,0,0,0,0],        #Quantity
                [0,0,0,0,0],        #Current
                [0,0,0,0,0]])       #Luminous intensity

#Delete null rows
D_mat = D_mat[D_mat.any(1)]

#get matrix dimensions
[d, k] = D_mat.shape

p = k-d
if p < 0:
    print ""  
    #Is the handling of systems with more dimensions than variables feasable 
    #when taking into account the function of this project?
else:
#Create righthand A-matrix and remove singularities
    A_det = 0

    while A_det == 0:
        A_mat = D_mat.T[p:k].T
        A_det = np.linalg.det(A_mat)
        A_rank = np.linalg.matrix_rank(A_mat)
        delta = d - A_rank
       
    
        if delta == 0 and A_det == 0:
#randomly swap two columns
            r = random.randint(0,k-1)
            D_mat[:,[0,1+r]] =  D_mat[:,[1+r,0]]
            print "shuffle"
        
        elif A_det == 0 and delta <> 0:
#remove singular rows and create new dimensional matrix
            u,s,v = np.linalg.svd(A_mat)
            D_mat = D_mat[s>1e-10]
            [d, k] = D_mat.shape
            p = k-d
            print "del"
#Create lefthand B-matrix
    B_mat = D_mat.T[0:p].T

#Create the E I matrix
    I_mat = np.identity(p)

#Create the E null patrix

    null_mat = np.zeros([p,d])

#Create the -inv(A)B submatrix

    A_inv = np.linalg.inv(A_mat)

    invAB_mat = dot(A_inv,B_mat)*-1
#Assemble the E matrix

    E_mat_top = np.concatenate((I_mat,null_mat),axis = 1)
    E_mat_bottom = np.concatenate((invAB_mat,A_inv),axis = 1)

    E_mat = np.concatenate((E_mat_top,E_mat_bottom),axis=0)

#Set up the Z matrix
#Added advantage that other groups (not non-dimensional) can be found
#simply by seting the last k rows to the desired type of dimensional group 
#power values For the non dimensional case they are simply set to zero

#create the q sub matrix for the non dimensional case

    q_mat = np.zeros([d,p])

#create the remaining non singular top Z sub matrix

    top_mat = np.array([[2,5],
                        [-1,0]])
##The problem now arises that since the top matrix has to be
## arbitratily chosen,One attempt was to use a simple identity matrix
## with dimension p which yielded valid dimensionless groups
## but not those desired.
## fixing the coefficients as they should be yields the correct final pi groups
#For this specific system
    Z_mat = np.concatenate((top_mat,q_mat),axis=0)


#the resulting P matrix columns represent the pi groups

    Pi_mat = around((dot(E_mat,Z_mat)),decimals = 2)
    
    [rows,cols] = Pi_mat.shape
# remove decimals
    
  #  for col in range(0,cols):
     #  print
      #  denom = np.zeros([rows,1])
        #for row in range(0,rows):
           # entry = Pi_mat[row,col]
            #denom[row] = Fraction(entry).limit_denominator(100).denominator
       # print GCD(denom.T)
            

    print Pi_mat
