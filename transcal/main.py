import math
#import sympy as sp
#from initialization import *
from parameters import *
from system_of_equations_copy import resolving_system_of_equations
import numpy as np

T_0 = np.full((M+1,N+1),(15+273))
i = 1
i_max = 1
T = [T_0]
np.savetxt('T_0.csv', T[0], delimiter=',', fmt='%.2f')
print(delta_x_b)
print(delta_y_a)
for i in range(i_max):
    system = resolving_system_of_equations(T,M,N,q_dot_0,alpha,h,T_inf,K,delta_t,i)
    #det = np.linalg.det(system[0])
    T_i1 = np.linalg.solve(system[0],system[1])
    for m in range (M+1):
        for n in range(N+1):
            k = m * (N+1) + n
            T[i][m][n] = T_i1[k]
    #print(T_i1)
    #print(det)
#print(A)
np.savetxt('A.csv', system[0], delimiter=',', fmt='%.2f')
np.savetxt('b.csv', system[1], delimiter=',', fmt='%.2f')
np.savetxt('T_i1_a.csv', T_i1, delimiter=',', fmt='%.2f')
np.savetxt('T_i1.csv', T[i], delimiter=',', fmt='%.2f')