from parameters import *

class Knot:
    def __init__(self, m, n):
        self.m = m
        self.n = n
        self.delta_x = delta_x
        self.delta_y = delta_y
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
            
        elif ((self.m == 0 and not (self.n == 0  or self.n == N)) or (self.m == M and not N_a <= self.n <= N_b) 
              or (self.n == 0 and not (self.m == 0 or self.m == M)) or 
              (self.n == N and not (self.m == 0 or self.m == M))): # group 2 - walls
            self.group = 2
            
            if self.m == 0 and not (self.n == 0  or self.n == N): # left wall - (0,n) knots
                self.group = self.group + 0.1
            
            elif self.m == M and not N_a <= self.n <= N_b: # right wall - (M,n) knots wih n < N_a or n > N_b
                self.group = self.group + 0.2
            
            elif self.n == 0 and not (self.m == 0 or self.m == M): # inferior wall - (m,0) knots
                self.group = self.group + 0.3
            
            elif self.n == N and not (self.m == 0 or self.m == M): # superior wall - (m,N) knots
                self.group = self.group + 0.4
        
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
        
        elif ((self.m == M_a and N_a < self.n < N_b) or (self.n == N_a and M_a < self.m < M_b) or 
              (self.n == N_b and M_a < self.m < M_b)): # group 4 - tube walls
            self.group = 4

            if self.m == M_a and N_a < self.n < N_b: # (M_a,n) knots with N_a < n < N_b
                self.group = self.group + 0.1
            elif self.n == N_a and M_a < self.m < M_b: # (m,N_a) knots with M_a < m < M_b
                self.group = self.group + 0.2
            elif self.n == N_b and M_a < self.m < M_b: # (m,N_b) knots with M_a < m < M_b
                self.group = self.group + 0.3
        
        elif self.m > M_a and N_a < self.n < N_b: # group 5 - water tubes
            self.group = 5
        
        else: # group 6 - interior
            self.group = 6
            
    def run(self):
        self.get_group()