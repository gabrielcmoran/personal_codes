from parameters import *
from system_of_equations_copy import system_of_equations
import numpy as np
import matplotlib.pyplot as plt

T_0 = np.full((M+1,N+1),(15+273),dtype=float)
i = 1
i_max = 10
T = [T_0]
np.savetxt('T_0.csv', T[0], delimiter=',', fmt='%.2f')
while i < i_max:
    T_i1_matrix = T[i-1]
    system = system_of_equations(T,M,N,q_dot_0,alpha,h,T_inf,K,delta_t,i)
    T_i1_array = np.linalg.solve(system[0],system[1])
    #print(T_i1_matrix)
    for m in range (M+1):
        for n in range(N+1):
            k = m * (N+1) + n
            T_i1_matrix[m][n] = T_i1_array[k]
    T.append(T_i1_matrix)
    i = i + 1
np.savetxt('A.csv', system[0], delimiter=',', fmt='%.2f')
np.savetxt('b.csv', system[1], delimiter=',', fmt='%.2f')
np.savetxt('T_i1_a.csv', T_i1_array, delimiter=',', fmt='%.4f')
np.savetxt('T_i1.csv', T_i1_matrix, delimiter=',', fmt='%.4f')

T_matrix = T[i-1]
T_matrix = T_matrix - 273
T_matrix = T_matrix[:, ::-1]
T_matrix = np.transpose(T_matrix)

plt.imshow(T_matrix, cmap='hot', interpolation='nearest')
cbar = plt.colorbar()
cbar.set_label('Temperatura [°C]')
plt.title("Distribuição de temperaturas")
plt.yticks(np.arange(len(T_matrix)), np.flip(np.arange(len(T_matrix))))
plt.show()