import numpy as np
from parameters import *
from knot import Knot
from scipy.sparse.linalg import spsolve
from scipy.sparse import csr_matrix

def system_of_equations(T_i0_array,M,N,q_dot,alpha,h,T_inf,K,delta_t,i):
    A = np.zeros(((M+1)*(N+1),(M+1)*(N+1)))
    b = np.zeros((M+1)*(N+1))
    k_q_dot_array = []
    area_q_dot_array = []
    m = 0
    n = 0

    for m in range(M+1):
        for n in range(N+1):
            knot = Knot(m,n)
            k = m * (N+1) + n

            if knot.group == 1.1:
                A[k][k] = - knot.delta_x/knot.delta_y - knot.delta_y/knot.delta_x - knot.delta_x*knot.delta_y/(2*alpha*delta_t)
                A[k][k+(N+1)] = knot.delta_y/knot.delta_x
                A[k][k+1] = knot.delta_x/knot.delta_y
                b[k] = - q_dot*knot.delta_x/K - knot.delta_x*knot.delta_y*T_i0_array[k]/(2*alpha*delta_t)
            
            elif knot.group == 1.2:
                A[k][k] = - knot.delta_x/knot.delta_y - knot.delta_y/knot.delta_x - knot.delta_x*knot.delta_y/(2*alpha*delta_t)
                A[k][k+(N+1)] = knot.delta_y/knot.delta_x
                A[k][k-1] = knot.delta_x/knot.delta_y
                b[k] = - knot.delta_x*knot.delta_y*T_i0_array[k]/(2*alpha*delta_t)
            
            elif knot.group == 1.3:
                A[k][k] = - knot.delta_x/knot.delta_y - knot.delta_y/knot.delta_x - knot.delta_x*knot.delta_y/(2*alpha*delta_t)
                A[k][k-(N+1)] = knot.delta_y/knot.delta_x
                A[k][k+1] = knot.delta_x/knot.delta_y
                b[k] = - q_dot*knot.delta_x/K - knot.delta_x*knot.delta_y*T_i0_array[k]/(2*alpha*delta_t)
            
            elif knot.group == 1.4:
                A[k][k] = - knot.delta_x/knot.delta_y - knot.delta_y/knot.delta_x - knot.delta_x*knot.delta_y/(2*alpha*delta_t)
                A[k][k-(N+1)] = knot.delta_y/knot.delta_x
                A[k][k-1] = knot.delta_x/knot.delta_y
                b[k] = - knot.delta_x*knot.delta_y*T_i0_array[k]/(2*alpha*delta_t)
            
            elif knot.group == 2.1:
                A[k][k] = - 2*knot.delta_x/knot.delta_y - 2*knot.delta_y/knot.delta_x - knot.delta_x*knot.delta_y/(alpha*delta_t)
                A[k][k+(N+1)] = 2*knot.delta_y/knot.delta_x
                A[k][k-1] = knot.delta_x/knot.delta_y
                A[k][k+1] = knot.delta_x/knot.delta_y
                b[k] = - knot.delta_x*knot.delta_y*T_i0_array[k]/(alpha*delta_t)
                
            elif knot.group == 2.2:
                A[k][k] = - 2*knot.delta_x/knot.delta_y - 2*knot.delta_y/knot.delta_x - knot.delta_x*knot.delta_y/(alpha*delta_t)
                A[k][k-(N+1)] = 2*knot.delta_y/knot.delta_x
                A[k][k-1] = knot.delta_x/knot.delta_y
                A[k][k+1] = knot.delta_x/knot.delta_y
                b[k] = - knot.delta_x*knot.delta_y*T_i0_array[k]/(alpha*delta_t)
            
            elif knot.group == 2.3:
                A[k][k] = - 2*knot.delta_x/knot.delta_y - 2*knot.delta_y/knot.delta_x - knot.delta_x*knot.delta_y/(alpha*delta_t)
                A[k][k+(N+1)] = knot.delta_y/knot.delta_x
                A[k][k-(N+1)] = knot.delta_y/knot.delta_x
                A[k][k+1] = 2*knot.delta_x/knot.delta_y
                b[k] = - 2*q_dot*knot.delta_x/K - knot.delta_x*knot.delta_y*T_i0_array[k]/(alpha*delta_t)

            elif knot.group == 2.4:
                A[k][k] = - 2*knot.delta_x/knot.delta_y - 2*knot.delta_y/knot.delta_x - knot.delta_x*knot.delta_y/(alpha*delta_t)
                A[k][k-(N+1)] = knot.delta_y/knot.delta_x
                A[k][k+(N+1)] = knot.delta_y/knot.delta_x
                A[k][k-1] = 2*knot.delta_x/knot.delta_y
                b[k] = - knot.delta_x*knot.delta_y*T_i0_array[k]/(alpha*delta_t)
            
            elif knot.group == 3.1:
                A[k][k] = (- 3*knot.delta_x/knot.delta_y - 3*knot.delta_y/knot.delta_x - h*(knot.delta_y + knot.delta_x)/K
                           -  3*knot.delta_y*knot.delta_x/(2*alpha*delta_t))
                A[k][k-(N+1)] = 2*knot.delta_y/knot.delta_x
                A[k][k+(N+1)] = knot.delta_y/knot.delta_x
                A[k][k+1] = knot.delta_x/knot.delta_y
                A[k][k-1] = 2*knot.delta_x/knot.delta_y
                b[k] = - h*(knot.delta_y + knot.delta_x)*T_inf/K - T_i0_array[k]*3*knot.delta_x*knot.delta_y/(2*alpha*delta_t)
                k_q_dot_array.append(k)
                area_q_dot_array.append((knot.delta_x/2 + knot.delta_y/2))
            
            elif knot.group == 3.2:
                A[k][k] = (- 3*knot.delta_x/knot.delta_y - 3*knot.delta_y/knot.delta_x - h*(knot.delta_y + knot.delta_x)/K
                           - 3*knot.delta_y*knot.delta_x/(2*alpha*delta_t))
                A[k][k-(N+1)] = 2*knot.delta_y/knot.delta_x
                A[k][k+(N+1)] = knot.delta_y/knot.delta_x
                A[k][k+1] = 2*knot.delta_x/knot.delta_y
                A[k][k-1] = knot.delta_x/knot.delta_y
                b[k] = - h*(knot.delta_y + knot.delta_x)*T_inf/K - T_i0_array[k]*3*knot.delta_x*knot.delta_y/(2*alpha*delta_t)
                k_q_dot_array.append(k)
                area_q_dot_array.append((knot.delta_x/2 + knot.delta_y/2))
            
            elif knot.group == 3.3:
                A[k][k] = - knot.delta_y/knot.delta_x - knot.delta_x/knot.delta_y - h*knot.delta_x/K - knot.delta_x*knot.delta_y/(2*alpha*delta_t)
                A[k][k-(N+1)] = knot.delta_y/knot.delta_x
                A[k][k-1] = knot.delta_x/knot.delta_y
                b[k] = - h*knot.delta_x*T_inf/K - knot.delta_x*knot.delta_y*T_i0_array[k]/(2*alpha*delta_t)
                k_q_dot_array.append(k)
                area_q_dot_array.append((knot.delta_x/2))
            
            elif knot.group == 3.4:
                A[k][k] = - knot.delta_y/knot.delta_x - knot.delta_x/knot.delta_y - h*knot.delta_x/K - knot.delta_x*knot.delta_y/(2*alpha*delta_t)
                A[k][k-(N+1)] = knot.delta_y/knot.delta_x
                A[k][k+1] = knot.delta_x/knot.delta_y
                b[k] = - h*knot.delta_x*T_inf/K - knot.delta_x*knot.delta_y*T_i0_array[k]/(2*alpha*delta_t)
                k_q_dot_array.append(k)
                area_q_dot_array.append((knot.delta_x/2))
            
            elif knot.group == 4.1:
                A[k][k] = - 2*knot.delta_x/knot.delta_y - 2*knot.delta_y/knot.delta_x - 2*h*knot.delta_y/K - knot.delta_x*knot.delta_y/(alpha*delta_t)
                A[k][k-(N+1)] = 2*knot.delta_y/knot.delta_x
                A[k][k-1] = knot.delta_x/knot.delta_y
                A[k][k+1] = knot.delta_x/knot.delta_y
                b[k] = - 2*h*knot.delta_y*T_inf/K - knot.delta_x*knot.delta_y*T_i0_array[k]/(alpha*delta_t)
                k_q_dot_array.append(k)
                area_q_dot_array.append((knot.delta_y))
            
            elif knot.group == 4.2:
                A[k][k] = - 2*knot.delta_y/knot.delta_x - 2*knot.delta_x/knot.delta_y - 2*h*knot.delta_x/K - knot.delta_x*knot.delta_y/(alpha*delta_t)
                A[k][k-(N+1)] = knot.delta_y/knot.delta_x
                A[k][k+(N+1)] = knot.delta_y/knot.delta_x
                A[k][k-1] = 2*knot.delta_x/knot.delta_y
                b[k] = -2*h*knot.delta_x*T_inf/K - knot.delta_x*knot.delta_y*T_i0_array[k]/(alpha*delta_t)
                k_q_dot_array.append(k)
                area_q_dot_array.append((knot.delta_x))
            
            elif knot.group == 4.3:
                A[k][k] = - 2*knot.delta_y/knot.delta_x - 2*knot.delta_x/knot.delta_y - 2*h*knot.delta_x/K - knot.delta_x*knot.delta_y/(alpha*delta_t)
                A[k][k-(N+1)] = knot.delta_y/knot.delta_x
                A[k][k+(N+1)] = knot.delta_y/knot.delta_x
                A[k][k+1] = 2*knot.delta_x/knot.delta_y
                b[k] = - 2*h*knot.delta_x*T_inf/K - knot.delta_x*knot.delta_y*T_i0_array[k]/(alpha*delta_t)
                k_q_dot_array.append(k)
                area_q_dot_array.append((knot.delta_x))

            elif knot.group == 5:
                A[k][k] = 1
                b[k] = (15+273)
            
            elif knot.group == 6:
                A[k][k] = - 2*knot.delta_x/knot.delta_y - 2*knot.delta_y/knot.delta_x - knot.delta_x*knot.delta_y/(alpha*delta_t)
                A[k][k-(N+1)] = knot.delta_y/knot.delta_x
                A[k][k+(N+1)] = knot.delta_y/knot.delta_x
                A[k][k-1] = knot.delta_x/knot.delta_y
                A[k][k+1] = knot.delta_x/knot.delta_y
                b[k] = - knot.delta_x*knot.delta_y*T_i0_array[k]/(alpha*delta_t)

    return A,b,k_q_dot_array,area_q_dot_array

def solving_system_of_equations(M,N,q_dot_0,alpha,h,T_inf,K,delta_t):
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
        T.append(T_i1_matrix)
        T_array.append(T_i1_array)
        i = i + 1
    time_needed_PR = delta_t*(i-1)

    return time_array,Q_dot_ratio_array,A_knot_temperature,B_knot_temperature,C_knot_temperature,D_knot_temperature,T,time_needed_PR