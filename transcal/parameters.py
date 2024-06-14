# dimensions
l_a = 5*(10**-3) # [m]
l_b = 5*(10**-3) # [m]
h_a = 8*(10**-3) # [m]
h_b = 8*(10**-3) # [m]
h_c = 4*(10**-3) # [m]

# data
K = 190 # termic conductivity [W/mK]
q_dot_0 = 1*(10**5) # heat flow [W/m²]
alpha = 75*(10**-6) # termic resistivity [m²/s]
h = 5000 # convection coefficient [W/m²K]
Ti = (15+273) # initial temperature [°C]
T_inf = (15+273) # [°C]

# discretization
delta_t = 1 # [s]
M = 10
N = 12

delta_x = (l_a+l_b)/M
delta_y = (h_a+h_b+h_c)/N
M_a = M/2
M_b = 2*M/2
N_a = N/3
N_b = 2*N/3
N_c = 3*N/3