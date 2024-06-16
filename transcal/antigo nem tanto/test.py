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
spacial_discretization(M,N,M_a,M_b,N_a,N_b,delta_x,delta_y,plot)