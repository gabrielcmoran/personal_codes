# Heat transmission work

import math
import sympy as sp

# dimensions
l_a = 5*(10**-3) # [m]
l_b = 10*(10**-3) # [m]
l_c = 5*(10**-3) # [m]
h_a = 8*(10**-3) # [m]
h_b = 8*(10**-3) # [m]
h_c = 4*(10**-3) # [m]

# data
k = 190 # termic conductivity [W/mK]
q_dot_0 = 10**5 # heat flow [W/m²]
alpha = 75*(10**-6) # termic resistivity [m²/s]
h = 5000 # convection coefficient [W/m²K]
Ti = 15 # initial temperature [°C]

# discretization
delta_t = 1 # [s]
M = 22
N = 22

M_a = math.floor(M/3)
M_b = M_a + math.floor(M/3)
M_c = M_b + math.floor(M/3)+ M%3

N_a = math.floor(N/3)
N_b = N_a + math.floor(N/3)
N_c = N_b + math.floor(N/3)+ N%3

delta_x_a = l_a/M_a
delta_x_b = l_b/(M_b - M_a)
delta_x_c = l_c/(M_c - M_b)

delta_y_a = h_a/N_a
delta_y_b = h_b/(N_b - N_a)
delta_y_c = h_c/(N_c - N_b)

# initialization
def temperature_matrix_initialization(M,N):
    T = [[[]]]
    i0 = 0

    for m in range(M):
        for n in range(N):
            T[i0][m][n] = Ti
    
    return T

class Knot:
    def __init__(self, m, n):
        self.m = m
        self.n = n
        self.run()
    
    def get_group(self):
        if ((self.m == 0 and self.n == 0) or (self.m == 0 and self.n == N) or 
            (self.m == M and self.n == 0) or (self.m == M and self.n == N)): # group 1 - cornes
            self.group = 1
            if self.m == 0 and self.n == 0: # (0,0) knot
                self.group = self.group + 0.1
            elif self.m == 0 and self.n == N: # (0,N) knot
                self.group = self.group + 0.2
            elif self.m == M and self.n == 0: # (M,0) knot
                self.group = self.group + 0.3
            elif self.m == M and self.n == N: # (M,N) knot
                self.group = self.group + 0.4
            
        elif ((self.m == 0) or (self.m == M) or (self.n == 0) or self.n == N): # group 2 - walls
            self.group = 2
            
            if self.m == 0: # left wall
                if self.n < N_a: # (0,n) knots with n < N_a
                    self.group = self.group + 0.11
                elif self.n == N_a: # (0,N_a) knot
                    self.group = self.group + 0.12
                elif N_a < self.n < N_b: # (0,n) knots with N_a < n < N_b
                    self.group = self.group + 0.13
                elif self.n == N_b: # (0,N_b) knot
                    self.group = self.group + 0.14
                if self.n > N_b: # (0,n) knots with n > N_b
                    self.group = self.group + 0.15
            
            elif self.m == M: # right wall
                if self.n < N_a: # (M,n) knots with n < N_a
                    self.group = self.group + 0.21
                elif self.n == N_a: # (M,N_a) knot
                    self.group = self.group + 0.22
                elif N_a < self.n < N_b: # (M,n) knots with N_a < n < N_b
                    self.group = self.group + 0.23
                elif self.n == N_b: # (M,N_b) knot
                    self.group = self.group + 0.24
                if self.n > N_b: # (M,n) knots with n > N_b
                    self.group = self.group + 0.25
            
            elif self.n == 0: # inferior wall
                if self.m < M_a: # (m,0) knots with m < M_a
                    self.group = self.group + 0.31
                elif self.m == M_a: # (M_a,0) knot
                    self.group = self.group + 0.32
                elif M_a < self.m < M_b: # (m,0) knots with M_a < m < M_b
                    self.group = self.group + 0.33
                elif self.m == M_b: # (M_b,0) knot
                    self.group = self.group + 0.34
                if self.m > M_b: # (m,0) knots with m > M_b
                    self.group = self.group + 0.35
            
            elif self.n == N: # superior wall
                if self.m < M_a: # (m,N) knots with m < M_a
                    self.group = self.group + 0.41
                elif self.m == M_a: # (M_a,N) knot
                    self.group = self.group + 0.42
                elif M_a < self.m < M_b: # (m,N) knots with M_a < m < M_b
                    self.group = self.group + 0.43
                elif self.m == M_b: # (M_b,N) knot
                    self.group = self.group + 0.44
                if self.m > M_b: # (m,N) knots with m > M_b
                    self.group = self.group + 0.45
        
        elif ((self.m == M_a and self.n == N_a) or (self.m == M_a and self.n == N_b) or 
              (self.m == M_b and self.n == N_a) or (self.m == M_b and self.n == N_b)): # group 3 - tube corners
            self.group = 3

            if self.m == M_a and self.n == N_a: # (M_a,N_a) knot
                self.group = self.group + 0.1
            elif self.m == M_a and self.n == N_b: # (M_a,N_b) knot
                self.group = self.group + 0.2
            elif self.m == M_b and self.n == N_a: # (M_b,N_a) knot
                self.group = self.group + 0.3
            elif self.m == M_b and self.n == N_b: # (M_b,N_b) knot
                self.group = self.group + 0.4
        
        elif ((self.m == M_a and N_a < self.n < N_b) or (self.m == M_b and N_a < self.n < N_b) or 
              (self.n == N_a and M_a < self.m < M_b) or (self.n == N_b and M_a < self.m < M_b)): # group 4 - tube walls
            self.group = 4

            if self.m == M_a and N_a < self.n < N_b: # (M_a,n) knots with N_a < n < N_b
                self.group = self.group + 0.1
            elif self.m == M_b and N_a < self.n < N_b: # (M_b,n) knots with N_a < n < N_b
                self.group = self.group + 0.2
            elif self.n == N_a and M_a < self.m < M_b: # (m,N_a) knots with M_a < m < M_b
                self.group = self.group + 0.3
            elif self.n == N_b and M_a < self.m < M_b: # (m,N_b) knots with M_a < m < M_b
                self.group = self.group + 0.4
        
        else: # group 5 - interior
            self.group = 5
            if self.m == M_a and self.n < N_a: # (M_a,n) knots with n < N_a
                self.group = self.group + 0.1
            elif self.m == M_a and self.n > N_b: # (M_a,n) knots with n > N_b
                self.group = self.group + 0.2
            elif self.m == M_b and self.n < N_a: # (M_b,n) knots with n < N_a
                self.group = self.group + 0.3
            elif self.m == M_b and self.n > N_b: # (M_b,n) knots with n > N_b
                self.group = self.group + 0.4
            elif self.n == N_a and self.m < M_a: # (m,N_a) knots with m < M_a
                self.group = self.group + 0.5
            elif self.n == N_a and self.m > M_b: # (m,N_a) knots with m > M_b
                self.group = self.group + 0.6
            elif self.n == N_b and self.m < M_a: # (m,N_b) knots with m < M_a
                self.group = self.group + 0.7
            elif self.n == N_b and self.m > M_b: # (m,N_b) knots with m > M_b
                self.group = self.group + 0.8
            elif self.m < M_a and self.n < N_a: # (m,n) knots with m < M_a and n < N_a
                self.group = self.group + 0.91
            elif self.m < M_a and N_a < self.n < N_b: # (m,n) knots with m < M_a and N_a < n < N_b
                self.group = self.group + 0.92
            elif self.m < M_a and self.n > N_b: # (m,n) knots with m < M_a and n > N_b
                self.group = self.group + 0.93
            elif M_a < self.m < M_b and self.n < N_a: # (m,n) knots with M_a < m < M_b and n < N_a
                self.group = self.group + 0.94
            elif M_a < self.m < M_b and self.n > N_b: # (m,n) knots with M_a < m < M_b and n > N_b
                self.group = self.group + 0.95
            elif self.m > M_b and self.n < N_a: # (m,n) knots with m > M_b and n < N_a
                self.group = self.group + 0.96
            elif self.m > M_b and N_a < self.n < N_b: # (m,n) knots with m > M_b and N_a < n < N_b
                self.group = self.group + 0.97
            elif self.m > M_b and self.n > N_b: # (m,n) knots with m > M_b and n > N_b
                self.group = self.group + 0.98
    
    def get_dimensions(self):
        if math.floor(self.group) == 1: # group 1
            if self.group == 1.1:
                self.delta_x = delta_x_a
                self.delta_y = delta_y_a
            elif self.group == 1.2:
                self.delta_x = delta_x_c
                self.delta_y = delta_y_a
            elif self.group == 1.3:
                self.delta_x = delta_x_a
                self.delta_y = delta_y_c
            elif self.group == 1.4:
                self.delta_x = delta_x_c
                self.delta_y = delta_y_c
        
        elif math.floor(self.group) == 2: # group 2
            if self.group == 2.11:
                self.delta_x = delta_x_a
                self.delta_y = delta_y_a
            elif self.group == 2.12:
                self.delta_x = delta_x_a
                self.delta_y = (delta_y_a + delta_y_b)/2
            elif self.group == 2.13:
                self.delta_x = delta_x_a
                self.delta_y = delta_y_b
            elif self.group == 2.14:
                self.delta_x = delta_x_a
                self.delta_y = (delta_y_b + delta_y_c)/2
            elif self.group == 2.15:
                self.delta_x = delta_x_a
                self.delta_y = delta_y_c
            
            elif self.group == 2.21:
                self.delta_x = delta_x_c
                self.delta_y = delta_y_a
            elif self.group == 2.22:
                self.delta_x = delta_x_c
                self.delta_y = (delta_y_a + delta_y_b)/2
            elif self.group == 2.23:
                self.delta_x = delta_x_c
                self.delta_y = delta_y_b
            elif self.group == 2.24:
                self.delta_x = delta_x_c
                self.delta_y = (delta_y_b + delta_y_c)/2
            elif self.group == 2.25:
                self.delta_x = delta_x_c
                self.delta_y = delta_y_c
            
            elif self.group == 2.31:
                self.delta_x = delta_x_a
                self.delta_y = delta_y_a
            elif self.group == 2.32:
                self.delta_x = (delta_x_a + delta_x_b)/2
                self.delta_y = delta_y_a
            elif self.group == 2.33:
                self.delta_x = delta_x_b
                self.delta_y = delta_y_a
            elif self.group == 2.34:
                self.delta_x = (delta_x_b + delta_x_c)/2
                self.delta_y = delta_y_a
            elif self.group == 2.35:
                self.delta_x = delta_x_c
                self.delta_y = delta_y_a
            
            elif self.group == 2.41:
                self.delta_x = delta_x_a
                self.delta_y = delta_y_c
            elif self.group == 2.42:
                self.delta_x = (delta_x_a + delta_x_b)/2
                self.delta_y = delta_y_c
            elif self.group == 2.43:
                self.delta_x = delta_x_b
                self.delta_y = delta_y_c
            elif self.group == 2.44:
                self.delta_x = (delta_x_b + delta_x_c)/2
                self.delta_y = delta_y_c
            elif self.group == 2.45:
                self.delta_x = delta_x_c
                self.delta_y = delta_y_c
        
        elif math.floor(self.group) == 3: # group 3
            if self.group == 3.1:
                self.delta_x_a = delta_x_a
                self.delta_x_b = delta_x_b
                self.delta_y_a = delta_y_a
                self.delta_y_b = delta_y_b
            elif self.group == 3.2:
                self.delta_x_a = delta_x_a
                self.delta_x_b = delta_x_b
                self.delta_y_b = delta_y_b
                self.delta_y_c = delta_y_c
            elif self.group == 3.3:
                self.delta_x_b = delta_x_b
                self.delta_x_c = delta_x_c
                self.delta_y_a = delta_y_a
                self.delta_y_b = delta_y_b
            elif self.group == 3.4:
                self.delta_x_b = delta_x_b
                self.delta_x_c = delta_x_c
                self.delta_y_b = delta_y_b
                self.delta_y_c = delta_y_c
        
        elif math.floor(self.group) == 4: # group 4
            if self.group == 4.1:
                self.delta_x = delta_x_a
                self.delta_y = delta_y_b
            elif self.group == 4.2:
                self.delta_x = delta_x_c
                self.delta_y = delta_y_b
            elif self.group == 4.3:
                self.delta_x = delta_x_b
                self.delta_y = delta_y_a
            elif self.group == 4.4:
                self.delta_x = delta_x_b
                self.delta_y = delta_y_c
            
        elif math.floor(self.group) == 5: # group 5
            if self.group == 5.1:
                self.delta_x = (delta_x_a + delta_x_b)/2
                self.delta_y = delta_y_a
            elif self.group == 5.2:
                self.delta_x = (delta_x_a + delta_x_b)/2
                self.delta_y = delta_y_c
            elif self.group == 5.3:
                self.delta_x = (delta_x_b + delta_x_c)/2
                self.delta_y = delta_y_a
            elif self.group == 5.4:
                self.delta_x = (delta_x_b + delta_x_c)/2
                self.delta_y = delta_y_c
            elif self.group == 5.5:
                self.delta_x = delta_x_a
                self.delta_y = (delta_y_a + delta_y_b)/2
            elif self.group == 5.6:
                self.delta_x = delta_x_c
                self.delta_y = (delta_y_a + delta_y_b)/2
            elif self.group == 5.7:
                self.delta_x = delta_x_a
                self.delta_y = (delta_y_b + delta_y_c)/2
            elif self.group == 5.8:
                self.delta_x = delta_x_c
                self.delta_y = (delta_y_b + delta_y_c)/2
            elif self.group == 5.91:
                self.delta_x = delta_x_a
                self.delta_y = delta_y_a
            elif self.group == 5.92:
                self.delta_x = delta_x_a
                self.delta_y = delta_y_b
            elif self.group == 5.93:
                self.delta_x = delta_x_a
                self.delta_y = delta_y_c
            elif self.group == 5.94:
                self.delta_x = delta_x_b
                self.delta_y = delta_y_a
            elif self.group == 5.95:
                self.delta_x = delta_x_b
                self.delta_y = delta_y_c
            elif self.group == 5.96:
                self.delta_x = delta_x_c
                self.delta_y = delta_y_a
            elif self.group == 5.97:
                self.delta_x = delta_x_c
                self.delta_y = delta_y_b
            elif self.group == 5.98:
                self.delta_x = delta_x_c
                self.delta_y = delta_y_c
            

    def get_equation(self):
        if math.floor(self.group) == 1: # group 1
            self.equation = ((self.delta_x/self.delta_y)*(T[0][1] - T[0][0]) + (self.delta_y/self.delta_x)*
                        (T[1][0] - T[0][0]) + q_dot_0*self.delta_x/k)
            self.equation_result = (1/2)*(self.delta_x*self.delta_y/alpha)*(T[0][0][i+1] - T[0][0][i])/delta_t

    def run(self):
        self.get_group()
        self.get_dimensions()
        self.get_equation()

knot = Knot(0,0)
print(knot.delta_x)