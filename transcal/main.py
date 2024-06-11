from parameters import *
from system_of_equations_copy import system_of_equations
import numpy as np
import matplotlib.pyplot as plt

T_0_matrix = np.full((M+1,N+1),(15+273),dtype=float)
T_0_array = np.full(((M+1)*(N+1),1),(15+273))
i = 1
i_max = 40
T = [T_0_matrix]
T_array = [T_0_array]
np.savetxt('T_0.csv', T[0], delimiter=',', fmt='%.2f')
time_array = []
q_dot_water_array = []
q_dot_ratio_array = []
#print(delta_x_a, delta_y_a)
while i < i_max:
    T_i1_matrix = T[i-1]
    T_i0_array = T_array[i-1]
    system = system_of_equations(T_i0_array,M,N,q_dot_0,alpha,h,T_inf,K,delta_t,i)
    T_i1_array = np.linalg.solve(system[0],system[1])
    k_q_dot_array = system[2]
    area_q_dot_array = system[3]
    q_dot_water_total = 0
    for m in range (M+1):
        for n in range(N+1):
            k = m * (N+1) + n
            T_i1_matrix[m][n] = T_i1_array[k]
    for item in k_q_dot_array:
        #print(item)
        index = k_q_dot_array.index(item)
        area_local = area_q_dot_array[index]
        #print(area_local)
        T_local = T_i1_array[item]
        #print(T_local)
        q_dot_local = h*area_local*(T_local - T_inf)
        q_dot_local = h*(T_local - T_inf)
        q_dot_water_total = q_dot_water_total + q_dot_local
    q_dot_ratio = q_dot_water_total/q_dot_0
    time_array.append((i*delta_t))
    q_dot_water_array.append(q_dot_water_total)
    q_dot_ratio_array.append(q_dot_ratio)
    np.savetxt('T_i1_a.csv', T_i1_array, delimiter=',', fmt='%.4f')
    np.savetxt('T_i1.csv', T_i1_matrix, delimiter=',', fmt='%.4f')
    T.append(T_i1_matrix)
    T_array.append(T_i1_array)
    i = i + 1
np.savetxt('A.csv', system[0], delimiter=',', fmt='%.2f')
np.savetxt('b.csv', system[1], delimiter=',', fmt='%.5f')
#np.savetxt('T_i1_a.csv', T_i1_array, delimiter=',', fmt='%.4f')
#np.savetxt('T_i1.csv', T_i1_matrix, delimiter=',', fmt='%.4f')

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

plot_b = 2
if plot_b == 1:
    plt.plot(time_array, q_dot_ratio_array)
    plt.show()


# SE O M FOR IMPAR, TA DANDO MERDA