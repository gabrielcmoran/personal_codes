import sympy as sp
import math

# Defina as variáveis
z = 4
x, y = sp.symbols('x, y')

# Defina as equações
equations = []
variables = []
variables.append(x)
variables.append(y)
variables.append(z)
eq1 = sp.Eq(x + x - 5*x + y + z, 0)
equations.append(eq1)
eq2 = sp.Eq(2*x + y - z, 3)
equations.append(eq2)
#eq3 = sp.Eq(x - y + z, 2)
#equations.append(eq3)
# Resolva o sistema de equações
solucoes = sp.solve(equations, variables)
print(solucoes)

eq3 = sp.Eq(x + x - 5*x + y, -4)
eq4 = sp.Eq(2*x + y, 7)
solucoes2 = sp.solve([eq3, eq4], variables)
print(solucoes2)



Ti = 15
M = 5
N = 5

def temperature_matrix_initialization(M,N,Ti):
    T_0 = []
    for m in range(M+1):
        T_line = []
        for n in range(N+1):
            T_line.append(Ti)
        T_0.append(T_line)
        Ti = Ti+1
    T = [T_0]
    return T

#T = temperature_matrix_initialization(M,N,Ti)