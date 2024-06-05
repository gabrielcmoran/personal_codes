from parameters import *

def temperature_matrix_initialization(M,N,Ti):
    T_0 = []
    for m in range(M+1):
        T_line = []
        for n in range(N+1):
            T_line.append(Ti)
        T_0.append(T_line)
        Ti = Ti+1
    T = [T_0]
    return T

T = temperature_matrix_initialization(M,N,Ti)