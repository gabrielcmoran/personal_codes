import numpy as np
import math
from knot import Knot

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
                A[k][k+(N+1)] = knot.delta_x/knot.delta_y
                A[k][k+1] = knot.delta_y/knot.delta_x
                #print(T_i0_array[k])
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
            
            elif 2.1 < knot.group < 2.2:
                A[k][k] = - 2*knot.delta_x/knot.delta_y - 2*knot.delta_y/knot.delta_x - knot.delta_x*knot.delta_y/(alpha*delta_t)
                A[k][k+(N+1)] = 2*knot.delta_y/knot.delta_x
                A[k][k-1] = knot.delta_x/knot.delta_y
                A[k][k+1] = knot.delta_x/knot.delta_y
                b[k] = - knot.delta_x*knot.delta_y*T_i0_array[k]/(alpha*delta_t)
                
            elif 2.2 < knot.group < 2.3:
                A[k][k] = - 2*knot.delta_x/knot.delta_y - 2*knot.delta_y/knot.delta_x - knot.delta_x*knot.delta_y/(alpha*delta_t)
                A[k][k-(N+1)] = 2*knot.delta_y/knot.delta_x
                A[k][k-1] = knot.delta_x/knot.delta_y
                A[k][k+1] = knot.delta_x/knot.delta_y
                b[k] = - knot.delta_x*knot.delta_y*T_i0_array[k]/(alpha*delta_t)
            
            elif 2.3 < knot.group < 2.4:
                A[k][k] = - knot.delta_x/knot.delta_y - 2*knot.delta_y/knot.delta_x - knot.delta_x*knot.delta_y/(alpha*delta_t)
                A[k][k+(N+1)] = knot.delta_y/knot.delta_x
                A[k][k+-1] = knot.delta_y/knot.delta_x
                A[k][k+1] = knot.delta_x/knot.delta_y
                b[k] = - 2*q_dot*knot.delta_x/K - knot.delta_x*knot.delta_y*T_i0_array[k]/(alpha*delta_t)
            
            elif 2.4 < knot.group < 2.5:
                A[k][k] = - 2*knot.delta_x/knot.delta_y - 2*knot.delta_y/knot.delta_x - knot.delta_x*knot.delta_y/(alpha*delta_t)
                A[k][k-(N+1)] = knot.delta_y/knot.delta_x
                A[k][k+(N+1)] = knot.delta_y/knot.delta_x
                A[k][k-1] = 2*knot.delta_x/knot.delta_y
                b[k] = - knot.delta_x*knot.delta_y*T_i0_array[k]/(alpha*delta_t)
            
            elif knot.group == 3.1:
                #print(knot.delta_x_a, knot.delta_x_b)
                #print(knot.delta_y_a, knot.delta_y_b)
                A[k][k] = (- knot.delta_x_a/knot.delta_y_a - (knot.delta_x_b + knot.delta_x_a)/knot.delta_y_a - knot.delta_y_a/knot.delta_x_b
                           - (knot.delta_y_b + knot.delta_y_a)/knot.delta_x_b - h*(knot.delta_y_b + knot.delta_x_b)/K
                           - (knot.delta_x_a*(knot.delta_y_b + knot.delta_y_a) + knot.delta_y_a*knot.delta_x_b)/(2*alpha*delta_t))
                A[k][k-(N+1)] = (knot.delta_y_b + knot.delta_y_a)/knot.delta_x_a
                A[k][k+(N+1)] = knot.delta_y_a/knot.delta_x_b
                A[k][k+1] = knot.delta_x_a/knot.delta_y_b
                A[k][k-1] = (knot.delta_x_b + knot.delta_x_a)/knot.delta_y_a
                b[k] = (- h*(knot.delta_y_b + knot.delta_x_b)*T_inf/K - T_i0_array[k]*(knot.delta_x_a*(knot.delta_y_b + knot.delta_y_a) + 
                                                                         knot.delta_y_a*knot.delta_x_b)/(2*alpha*delta_t))
                k_q_dot_array.append(k)
                area_q_dot_array.append((knot.delta_x_b/2 + knot.delta_y_b/2))
                print((knot.delta_x_a*(knot.delta_y_b + knot.delta_y_a) + knot.delta_y_a*knot.delta_x_b))
            
            elif knot.group == 3.2:
                A[k][k] = (- knot.delta_x_a/knot.delta_y_b - (knot.delta_x_a + knot.delta_x_b)/knot.delta_y_c - knot.delta_y_c/knot.delta_x_b
                           - (knot.delta_y_c + knot.delta_y_b)/knot.delta_x_a - h*(knot.delta_y_b + knot.delta_x_b)/K
                           - (knot.delta_x_a*(knot.delta_y_b + knot.delta_y_c) + knot.delta_y_c*knot.delta_x_b)/(2*alpha*delta_t))
                A[k][k-(N+1)] = (knot.delta_y_c + knot.delta_y_b)/knot.delta_x_a
                A[k][k+(N+1)] = knot.delta_y_c/knot.delta_x_b
                A[k][k+1] = (knot.delta_x_a + knot.delta_x_b)/knot.delta_y_c
                A[k][k-1] = knot.delta_x_a/knot.delta_y_b
                b[k] = (- h*(knot.delta_y_b + knot.delta_x_b)*T_inf/K - T_i0_array[k]*(knot.delta_x_a*(knot.delta_y_b + knot.delta_y_c) + 
                                                                         knot.delta_y_c*knot.delta_x_b)/(2*alpha*delta_t))
                k_q_dot_array.append(k)
                area_q_dot_array.append((knot.delta_x_b/2 + knot.delta_y_b/2))
            
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
                #b[k] = 15
            
            elif math.floor(knot.group) == 6:
                A[k][k] = - 2*knot.delta_x/knot.delta_y - 2*knot.delta_y/knot.delta_x - knot.delta_x*knot.delta_y/(alpha*delta_t)
                A[k][k-(N+1)] = knot.delta_y/knot.delta_x
                A[k][k+(N+1)] = knot.delta_y/knot.delta_x
                A[k][k-1] = knot.delta_x/knot.delta_y
                A[k][k+1] = knot.delta_x/knot.delta_y
                b[k] = - knot.delta_x*knot.delta_y*T_i0_array[k]/(alpha*delta_t)

    return A,b,k_q_dot_array,area_q_dot_array