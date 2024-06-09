import numpy as np
import math

def resolving_system_of_equations(T,knot,M,N):
    A = np.zeros((M*N,M*N))
    b = np.zeros(M*N)
    m = 0
    n = 0

    for m in range(M):
        for n in range(N):
            k = m * N + n

            if knot.group == 1.1:
                A[k][k] = 1
                A[k][k+1] = 2
                A[k][k-(N+1)] = 3
                b[k] = 4
            
            elif knot.group == 1.2:
                A[k][k] = 1
                A[k][k+1] = 2
                A[k][k+(N+1)] = 3
                b[k] = 4
            
            elif knot.group == 1.3:
                A[k][k] = 1
                A[k][k-1] = 2
                A[k][k-(N+1)] = 3
                b[k] = 4
            
            elif knot.group == 1.4:
                A[k][k] = 1
                A[k][k-1] = 2
                A[k][k+(N+1)] = 3
                b[k] = 4
            
            elif knot.group == 2.11:
                A[k][k] = 1
                A[k][k+1] = 2
                A[k][k+(N+1)] = 3
                A[k][k-(N+1)] = 3
                b[k] = 4
            
            elif knot.group == 2.12:
                A[k][k] = 1
                A[k][k+1] = 2
                A[k][k+(N+1)] = 3
                A[k][k-(N+1)] = 3
                b[k] = 4
            
            elif knot.group == 2.13:
                A[k][k] = 1
                A[k][k+1] = 2
                A[k][k+(N+1)] = 3
                A[k][k-(N+1)] = 3
                b[k] = 4
            
            elif knot.group == 2.14:
                A[k][k] = 1
                A[k][k+1] = 2
                A[k][k+(N+1)] = 3
                A[k][k-(N+1)] = 3
                b[k] = 4
            
            elif knot.group == 2.15:
                A[k][k] = 1
                A[k][k+1] = 2
                A[k][k+(N+1)] = 3
                A[k][k-(N+1)] = 3
                b[k] = 4
            
            elif knot.group == 2.21:
                A[k][k] = 1
                A[k][k-1] = 2
                A[k][k+(N+1)] = 3
                A[k][k-(N+1)] = 3
                b[k] = 4
            
            elif knot.group == 2.22:
                A[k][k] = 1
                A[k][k-1] = 2
                A[k][k+(N+1)] = 3
                A[k][k-(N+1)] = 3
                b[k] = 4
            
            elif knot.group == 2.31:
                A[k][k] = 1
                A[k][k-1] = 2
                A[k][k+1] = 2
                A[k][k-(N+1)] = 3
                b[k] = 4
            
            elif knot.group == 2.32:
                A[k][k] = 1
                A[k][k-1] = 2
                A[k][k+1] = 2
                A[k][k-(N+1)] = 3
                b[k] = 4
            
            elif knot.group == 2.33:
                A[k][k] = 1
                A[k][k-1] = 2
                A[k][k+1] = 2
                A[k][k-(N+1)] = 3
                b[k] = 4
            
            elif knot.group == 2.41:
                A[k][k] = 1
                A[k][k-1] = 2
                A[k][k+1] = 2
                A[k][k+(N+1)] = 3
                b[k] = 4
            
            elif knot.group == 2.42:
                A[k][k] = 1
                A[k][k-1] = 2
                A[k][k+1] = 2
                A[k][k+(N+1)] = 3
                b[k] = 4
            
            elif knot.group == 2.43:
                A[k][k] = 1
                A[k][k-1] = 2
                A[k][k+1] = 2
                A[k][k+(N+1)] = 3
                b[k] = 4
            
            elif knot.group == 3.1:
                A[k][k] = 1
                A[k][k-1] = 2
                A[k][k+1] = 2
                A[k][k-(N+1)] = 3
                A[k][k+(N+1)] = 3
                b[k] = 4
            
            elif knot.group == 3.2:
                A[k][k] = 1
                A[k][k-1] = 2
                A[k][k+1] = 2
                A[k][k-(N+1)] = 3
                A[k][k+(N+1)] = 3
                b[k] = 4
            
            elif knot.group == 3.3:
                A[k][k] = 1
                A[k][k-1] = 2
                A[k][k+(N+1)] = 3
                b[k] = 4
            
            elif knot.group == 3.4:
                A[k][k] = 1
                A[k][k-1] = 2
                A[k][k+(N+1)] = 3
                b[k] = 4
            
            elif knot.group == 4.1:
                A[k][k] = 1
                A[k][k-1] = 2
                A[k][k+(N+1)] = 3
                A[k][k-(N+1)] = 3
                b[k] = 4
            
            elif knot.group == 4.2:
                A[k][k] = 1
                A[k][k-1] = 2
                A[k][k+1] = 2
                A[k][k+(N+1)] = 3
                b[k] = 4
            
            elif knot.group == 4.3:
                A[k][k] = 1
                A[k][k-1] = 2
                A[k][k+1] = 2
                A[k][k-(N+1)] = 3
                b[k] = 4

            elif knot.group == 5:
                A[k][k] = 1
                b[k] = 2
            
            elif math.floor(knot.group) == 6:
                A[k][k] = 1
                A[k][k-1] = 2
                A[k][k+1] = 2
                A[k][k+(N+1)] = 3
                A[k][k-(N+1)] = 3
                b[k] = 4
                
            


    b_new = np.linalg.solve(A, b)
    #b_new = 
    return A,b,b_new