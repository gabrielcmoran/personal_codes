from parameters import *
from system_of_equations import system_of_equations
import numpy as np
import matplotlib.pyplot as plt
from spacial_discretization import spacial_discretization
from scipy.sparse.linalg import spsolve
from scipy.sparse import csr_matrix

T_0_matrix = np.full((M+1,N+1),(15+273),dtype=float)
T_0_array = np.full(((M+1)*(N+1),1),(15+273),dtype=float)
i = 1
i_max = 30
T = [T_0_matrix]
T_array = [T_0_array]
time_array = []
Q_dot_water_array = []
Q_dot_ratio_array = []
#print(delta_x, delta_y)
while i < i_max:
    T_i1_matrix = T[i-1]
    T_i0_array = T_array[i-1]
    system = system_of_equations(T_i0_array,M,N,q_dot_0,alpha,h,T_inf,K,delta_t,i)
    #print(f'(0,0): k,k: {system[0][0][0]}, k,k+1: {system[0][0][1]}, k,k+(N+1): {system[0][0][13]}, b(k): {system[1][0]}')
    #print(f'(M,0): k,k: {system[0][130][130]}, k,k+1: {system[0][130][131]}, k,k-(N+1): {system[0][130][117]}, b(k): {system[1][130]}')
    #T_i1_array = np.linalg.lstsq(system[0],system[1], rcond=None)
    A_csr = csr_matrix(system[0])
    T_i1_array = spsolve(A_csr,system[1])
    #print(f'(0,0): {T_i1_array[0]}')
    #print(f'(M,0): {T_i1_array[130]}')
    #print(T_i1_array)
    k_q_dot_array = system[2]
    area_q_dot_array = system[3]
    for m in range (M+1):
        for n in range(N+1):
            k = m * (N+1) + n
            T_i1_matrix[m][n] = T_i1_array[k]
    Q_dot_water_total = 0
    for item in k_q_dot_array:
        index = k_q_dot_array.index(item)
        area_local = area_q_dot_array[index]
        T_local = T_i1_array[item]
        Q_dot_local = h*area_local*(T_local - T_inf)
        Q_dot_water_total = Q_dot_water_total + Q_dot_local
    Q_dot_ratio = Q_dot_water_total/(q_dot_0*(l_a+l_b))
    time_array.append((i*delta_t))
    Q_dot_water_array.append(Q_dot_water_total)
    Q_dot_ratio_array.append(Q_dot_ratio)
    np.savetxt('T_i1_a.csv', T_i1_array, delimiter=',', fmt='%.4f')
    np.savetxt('T_i1.csv', T_i1_matrix, delimiter=',', fmt='%.4f')
    T.append(T_i1_matrix)
    T_array.append(T_i1_array)
    i = i + 1
np.savetxt('Ai.csv', system[0], delimiter=',', fmt='%.2f')
np.savetxt('bi.csv', system[1], delimiter=',', fmt='%.5f')
#np.savetxt('T_i1_a.csv', T_i1_array, delimiter=',', fmt='%.4f')
#np.savetxt('T_i1.csv', T_i1_matrix, delimiter=',', fmt='%.4f')
np.savetxt('T_0_a.csv', T_0_array, delimiter=',', fmt='%.4f')

plot_a = 1
if plot_a == 1:
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

plot_b = 1
if plot_b == 1:
    plt.plot(time_array, Q_dot_ratio_array)
    plt.show()

plot_c = 2
if plot_c == 1:
    spacial_discretization = spacial_discretization(M,N,M_a,M_b,N_a,N_b,delta_x,delta_y,plot_c)