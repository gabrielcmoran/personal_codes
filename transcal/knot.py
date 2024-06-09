import math
from parameters import *
from initialization import T,i
import sympy as sp

#i = 0 # ---------- verificar

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
                if self.n > N_b: # (M,n) knots with n > N_b
                    self.group = self.group + 0.22
            
            elif self.n == 0: # inferior wall
                if self.m < M_a: # (m,0) knots with m < M_a
                    self.group = self.group + 0.31
                elif self.m == M_a: # (M_a,0) knot
                    self.group = self.group + 0.32
                if self.m > M_a: # (m,0) knots with m > M_a
                    self.group = self.group + 0.33
            
            elif self.n == N: # superior wall
                if self.m < M_a: # (m,N) knots with m < M_a
                    self.group = self.group + 0.41
                elif self.m == M_a: # (M_a,N) knot
                    self.group = self.group + 0.42
                if self.m > M_a: # (m,N) knots with m > M_a
                    self.group = self.group + 0.43
        
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
            if self.m == M_a and self.n < N_a: # (M_a,n) knots with n < N_a
                self.group = self.group + 0.1
            elif self.m == M_a and self.n > N_b: # (M_a,n) knots with n > N_b
                self.group = self.group + 0.2
            elif self.n == N_a and self.m < M_a: # (m,N_a) knots with m < M_a
                self.group = self.group + 0.3
            elif self.n == N_b and self.m < M_a: # (m,N_b) knots with m < M_a
                self.group = self.group + 0.4
            elif self.m < M_a and self.n < N_a: # (m,n) knots with m < M_a and n < N_a
                self.group = self.group + 0.51
            elif self.m < M_a and N_a < self.n < N_b: # (m,n) knots with m < M_a and N_a < n < N_b
                self.group = self.group + 0.52
            elif self.m < M_a and self.n > N_b: # (m,n) knots with m < M_a and n > N_b
                self.group = self.group + 0.53
            elif self.m > M_a and self.n < N_a: # (m,n) knots with M_a < m < M_b and n < N_a
                self.group = self.group + 0.54
            elif self.m > M_a and self.n > N_b: # (m,n) knots with M_a < m < M_b and n > N_b
                self.group = self.group + 0.55
    
    def get_dimensions(self):
        if math.floor(self.group) == 1: # group 1
            if self.group == 1.1:
                self.delta_x = delta_x_a
                self.delta_y = delta_y_a
            elif self.group == 1.2:
                self.delta_x = delta_x_a
                self.delta_y = delta_y_c
            elif self.group == 1.3:
                self.delta_x = delta_x_b
                self.delta_y = delta_y_a
            elif self.group == 1.4:
                self.delta_x = delta_x_b
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
                self.delta_x = delta_x_b
                self.delta_y = delta_y_a
            elif self.group == 2.22:
                self.delta_x = delta_x_b
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
            
            elif self.group == 2.41:
                self.delta_x = delta_x_a
                self.delta_y = delta_y_c
            elif self.group == 2.42:
                self.delta_x = (delta_x_a + delta_x_b)/2
                self.delta_y = delta_y_c
            elif self.group == 2.43:
                self.delta_x = delta_x_b
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
                self.delta_x = delta_x_b
                self.delta_y = delta_y_a
            elif self.group == 3.4:
                self.delta_x = delta_x_b
                self.delta_y = delta_y_c
        
        elif math.floor(self.group) == 4: # group 4
            if self.group == 4.1:
                self.delta_x = delta_x_a
                self.delta_y = delta_y_b
            elif self.group == 4.2:
                self.delta_x = delta_x_b
                self.delta_y = delta_y_a
            elif self.group == 4.3:
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
                self.delta_x = delta_x_a
                self.delta_y = (delta_y_a + delta_y_b)/2
            elif self.group == 5.4:
                self.delta_x = delta_x_a
                self.delta_y = (delta_y_b + delta_y_c)/2
            elif self.group == 5.51:
                self.delta_x = delta_x_a
                self.delta_y = delta_y_a
            elif self.group == 5.52:
                self.delta_x = delta_x_a
                self.delta_y = delta_y_b
            elif self.group == 5.53:
                self.delta_x = delta_x_a
                self.delta_y = delta_y_c
            elif self.group == 5.54:
                self.delta_x = delta_x_b
                self.delta_y = delta_y_a
            elif self.group == 5.55:
                self.delta_x = delta_x_b
                self.delta_y = delta_y_c
            
    def run(self):
        self.get_group()
        self.get_dimensions()