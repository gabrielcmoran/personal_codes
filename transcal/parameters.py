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
N = 15

delta_x = (l_a+l_b)/M
delta_y = (h_a+h_b+h_c)/N
M_a = M/2
M_b = 2*M/2
N_a = N/2.5
N_b = 2*N/2.5
N_c = N_b + N/5

# evalueted knots
A_knot_position_x = (l_a+l_b)
A_knot_position_y = 0
A_knot_m = int(A_knot_position_x/delta_x)
A_knot_n = int(A_knot_position_y/delta_y)
B_knot_position_x = 0
B_knot_position_y = (12*10**-3)
B_knot_m = int(B_knot_position_x/delta_x)
B_knot_n = int(B_knot_position_y/delta_y)
C_knot_position_x = (l_a+l_b)
C_knot_position_y = (h_a+h_b+h_c)
C_knot_m = int(C_knot_position_x/delta_x)
C_knot_n = int(C_knot_position_y/delta_y)
D_knot_position_x = 0
D_knot_position_y = 0
D_knot_m = int(D_knot_position_x/delta_x)
D_knot_n = int(D_knot_position_y/delta_y)