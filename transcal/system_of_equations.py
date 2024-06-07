import numpy as np

def resolving_system_of_equations(T,knot,M,N):
    A = np.zeros((M*N,M*N))
    b = np.zeros(M*N)
    m = 0
    n = 0

    for m in range(M):
        for n in range(N):
            k = m * N + n
            #A[k,k]		coef do nó do momento
            #A[k,k-1]		coef do nó da esq
            #A[k,k+1]		coef do nó da dir
            #A[k,k+(n+1)]		coef nó de baixo
            #A[k,k-(n+1)]		coef nó de cima

            if knot.group == 1.1:
                A[k][k] = 1
                A[k][k+1] = 2
                A[k][k-(N+1)] = 3
                b[k] = 4
            
            if knot.group == 1.2:
                A[k][k] = 1
                A[k][k+1] = 2
                A[k][k+(N+1)] = 3
                b[k] = 4


    b_new = np.linalg.solve(A, b)
    #b_new = 
    return A,b,b_new