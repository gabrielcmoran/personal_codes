import math
import sympy as sp
from knot import Knot
import numpy as np
from spacial_discretization import spacial_discretization
from parameters import *

            #A[k,k]		coef do nó do momento
            #A[k,k-1]		coef do nó da esq
            #A[k,k+1]		coef do nó da dir
            #A[k,k+(n+1)]		coef nó de baixo
            #A[k,k-(n+1)]		coef nó de cima
plot = 1
delta_t_max = (delta_x**2)*(delta_y**2)/(2*alpha*((delta_x**2) + (delta_y**2)))
print(delta_t_max)

delta_t = 0.004
Ti1 = 2*alpha*delta_t*((1/delta_y**2)*288 + (1/delta_x**2)*288 - ((delta_x**2 + delta_y**2)/(delta_x**2*delta_y**2))*288 + q_dot_0*delta_x/2) + 288
print(Ti1)