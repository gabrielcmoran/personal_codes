from parameters import *
from system_of_equations import solving_system_of_equations
from plots import *

solving = solving_system_of_equations(M,N,q_dot_0,alpha,h,T_inf,K,delta_t)
spacial_discretization(M,N,M_a,M_b,N_a,N_b,delta_x,delta_y)
plot_Q_dot_ratio(solving[0],solving[1],solving[7])
evalueted_knots_temperature(solving[0],solving[2],solving[3],solving[4],solving[5])
generate_temperature_gif(solving[6],M)