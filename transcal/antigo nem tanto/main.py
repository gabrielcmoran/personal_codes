from parameters import *
from system_of_equations import system_of_equations
import numpy as np
import matplotlib.pyplot as plt
import imageio.v2 as imageio
from spacial_discretization import spacial_discretization
from scipy.sparse.linalg import spsolve
from scipy.sparse import csr_matrix

T_0_matrix = np.full((M+1,N+1),(15+273),dtype=float)
T_0_array = np.full(((M+1)*(N+1),1),(15+273),dtype=float)
i = 1
T = [T_0_matrix]
T_array = [T_0_array]
time_array = []
Q_dot_water_array = []
Q_dot_ratio_array = []
A_knot_temperature = []
B_knot_temperature = []
C_knot_temperature = []
D_knot_temperature = []
Q_dot_ratio = 0
Q_dot_ratio_min = 0.999

while Q_dot_ratio < Q_dot_ratio_min:
    T_i1_matrix = np.full((M+1,N+1),(15+273),dtype=float)
    T_i0_array = T_array[i-1]
    system = system_of_equations(T_i0_array,M,N,q_dot_0,alpha,h,T_inf,K,delta_t,i)
    A_csr = csr_matrix(system[0])
    T_i1_array = spsolve(A_csr,system[1])
    k_q_dot_array = system[2]
    area_q_dot_array = system[3]
    
    for m in range (M+1):
        for n in range(N+1):
            k = m * (N+1) + n
            T_i1_matrix[m][n] = T_i1_array[k]
    
    A_knot_temperature.append(T_i1_matrix[A_knot_m][A_knot_n] - 273)
    B_knot_temperature.append(T_i1_matrix[B_knot_m][B_knot_n] - 273)
    C_knot_temperature.append(T_i1_matrix[C_knot_m][C_knot_n] - 273)
    D_knot_temperature.append(T_i1_matrix[D_knot_m][D_knot_n] - 273)

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

plot_a = 2
if plot_a == 1:
    #i = i_max - 1
    T_matrix = T[i]
    T_matrix = T_matrix - 273
    T_matrix = T_matrix[:, ::-1]
    T_matrix = np.transpose(T_matrix)
    plt.imshow(T_matrix, cmap='hot', interpolation='nearest')
    cbar = plt.colorbar()
    cbar.set_label('Temperatura [°C]')
    plt.title("Distribuição de temperaturas")
    #plt.yticks(np.arange(len(T_matrix)), np.flip(np.arange(len(T_matrix)), 4))
    plt.yticks(np.arange(0, T_matrix.shape[0], 4), np.flip(np.arange(0, T_matrix.shape[0], 4)))
    plt.xticks(np.arange(0, M, 2))
    plt.show()

plot_b = 1
if plot_b == 1:
    plt.plot(time_array, Q_dot_ratio_array)
    plt.xlabel('Tempo [s]')
    plt.ylabel('Razão')
    plt.title('Razão entre as taxas de transferência de calor')
    plt.savefig('ratio.png', bbox_inches='tight')
    plt.show()

plot_c = 2
if plot_c == 1:
    spacial_discretization = spacial_discretization(M,N,M_a,M_b,N_a,N_b,delta_x,delta_y,plot_c)

plot_d = 2
if plot_d == 1:
    plt.plot(time_array, A_knot_temperature, label='Nó A')
    plt.plot(time_array, B_knot_temperature, label='Nó B')
    plt.plot(time_array, C_knot_temperature, label='Nó C')
    plt.plot(time_array, D_knot_temperature, label='Nó D')
    plt.xlabel('Tempo [s]')
    plt.ylabel('Temperatura [°C]')
    plt.title('Temperatura dos nós avaliados')
    plt.legend()
    plt.savefig('knots.png', bbox_inches='tight')
    plt.show()

def generate_temperature_plot(T_matrix,i):
    T_matrix = T_matrix - 273
    T_matrix = T_matrix[:, ::-1]
    T_matrix = np.transpose(T_matrix)
    plt.imshow(T_matrix, cmap='hot', interpolation='nearest', vmin=15, vmax=33)
    cbar = plt.colorbar()
    cbar.set_label('Temperatura [°C]')
    plt.title("Distribuição de temperaturas")
    plt.yticks(np.arange(0, T_matrix.shape[0], 4), np.flip(np.arange(0, T_matrix.shape[0], 4)))
    plt.xticks(np.arange(0, M, 2))
    filename = f'images/figure_{i}.png'
    filenames.append(filename)
    plt.savefig(filename, bbox_inches='tight')
    plt.close()

def generate_temperature_gif(T):
    for i in range(len(T)):
        print(i)
        T_matrix = T[i]
        generate_temperature_plot(T_matrix,i)
    with imageio.get_writer('temperature_gif.gif', fps=3) as writer:
        for filename in filenames:
            print(filename)
            image = imageio.imread(filename)
            writer.append_data(image)
        image = imageio.imread(f'images/figure_29.png')
        writer.append_data(image)

plot_e = 1
if plot_e == 1:
    filenames = []
    generate_temperature_gif(T)