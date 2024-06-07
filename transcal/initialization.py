from parameters import *
import numpy as np

def temperature_matrix_initialization(M,N,Ti):
    T_0 = []
    for m in range(M):
        T_line = []
        for n in range(N):
            T_line.append(Ti)
        T_0.append(T_line)
        Ti = Ti+1
    T = [T_0, T_0]
    
    return T

T = temperature_matrix_initialization(M,N,Ti)
i = 0

def temperature_matrix_increase(T,i):
    T_increase = T[i-1]
    T.append(T_increase)
    return T

#T = temperature_matrix_increase(T,i)