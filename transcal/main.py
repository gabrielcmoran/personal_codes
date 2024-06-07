import math
#import sympy as sp
from initialization import *
from parameters import *
from system_of_equations import resolving_system_of_equations
from knot import Knot
import numpy as np

knot = Knot(0,0)
T = np.full((M,N),15)
#print(knot.group)
i = 1
#T = temperature_matrix_initialization(M,N,Ti)

#while i < 2:
#    T = temperature_matrix_increase(T,i)
#    i = i + 1

print(T)

#A = resolving_system_of_equations(T, knot, M, N)[0]
#b = resolving_system_of_equations(T, knot, M, N)[1]
#b_new = resolving_system_of_equations(T, knot, M, N)[2]
#print(A)
#print(b)
#print(b_new)

A = [[1,1,1], [2,2,4], [3,3,3]]
print(A[1][2])