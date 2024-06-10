import math

# dimensions
l_a = 5*(10**-3) # [m]
l_b = 5*(10**-3) # [m]
h_a = 8*(10**-3) # [m]
h_b = 8*(10**-3) # [m]
h_c = 4*(10**-3) # [m]

# data
K = 190 # termic conductivity [W/mK]
q_dot_0 = 10**5 # heat flow [W/m²]
alpha = 75*(10**-6) # termic resistivity [m²/s]
h = 5000 # convection coefficient [W/m²K]
Ti = (15+273) # initial temperature [°C]
T_inf = (15+273) # [°C]

# discretization
delta_t = 3 # [s]
M = 16
N = 16

M_a = math.floor(M/2)
M_b = M_a + math.floor(M/2) + M%2

N_a = math.floor(N/3)
N_b = N_a + math.floor(N/3)
N_c = N_b + math.floor(N/3)+ N%3

delta_x_a = l_a/M_a
delta_x_b = l_b/(M_b - M_a)

delta_y_a = h_a/N_a
delta_y_b = h_b/(N_b - N_a)
delta_y_c = h_c/(N_c - N_b)