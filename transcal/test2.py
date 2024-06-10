import math
import sympy as sp
from knot import Knot
import numpy as np

# dimensions
l_a = 5*(10**-3) # [m]
l_b = 5*(10**-3) # [m]
h_a = 8*(10**-3) # [m]
h_b = 8*(10**-3) # [m]
h_c = 4*(10**-3) # [m]

# data
k = 190 # termic conductivity [W/mK]
q_dot_0 = 10**5 # heat flow [W/m²]
alpha = 75*(10**-6) # termic resistivity [m²/s]
h = 5000 # convection coefficient [W/m²K]
Ti = 15 # initial temperature [°C]

# discretization
delta_t = 1 # [s]
M = 22
N = 22

M_a = math.floor(M/3)
M_b = M_a + math.floor(M/3)
M_c = M_b + math.floor(M/3)+ M%3

N_a = math.floor(N/3)
N_b = N_a + math.floor(N/3)
N_c = N_b + math.floor(N/3)+ N%3

delta_x_a = l_a/M_a
delta_x_b = l_b/(M_b - M_a)

delta_y_a = h_a/N_a
delta_y_b = h_b/(N_b - N_a)
delta_y_c = h_c/(N_c - N_b)

            #A[k,k]		coef do nó do momento
            #A[k,k-1]		coef do nó da esq
            #A[k,k+1]		coef do nó da dir
            #A[k,k+(n+1)]		coef nó de baixo
            #A[k,k-(n+1)]		coef nó de cima
