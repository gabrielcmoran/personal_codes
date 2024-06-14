import matplotlib.pyplot as plt

def spacial_discretization(M,N,M_a,M_b,N_a,N_b,delta_x,delta_y,plot):
    x_array = []
    y_array = []
    n_array = []
    m_array = []
    m_division_array = []
    n_division_array = []
    a = True
    for m in range (M+1):
        for n in range(N+1):
            x_position = m*delta_x*10**3
            y_position = n*delta_y*10**3
            if m != M:
                m_division = m + 0.5
            if n != N:
                n_division = n + 0.5
            x_array.append(x_position)
            y_array.append(y_position)
            m_array.append(m)
            n_array.append(n)
            if a == True:
                n_division_array.append(n_division)
        m_division_array.append(m_division)
        a =  False
    if plot == 1:
        #plt.scatter(x_array, y_array)
        #plt.xlim(0,10)
        #plt.ylim(0,20)
        #plt.plot([5, 5], [8, 16], color='black')
        #plt.plot([5, 10], [8, 8], color='black')
        #plt.plot([5, 10], [16, 16], color='black')
        #plt.xlabel('Posição em x [mm]')
        #plt.ylabel('Posição em y [mm]')
        
        plt.scatter(m_array, n_array,s=50)
        plt.xlim(0,M)
        plt.ylim(0,N)
        plt.plot([M_a, M_a], [N_a, N_b], color='black', linewidth=3)
        plt.plot([M_a, M_b], [N_a, N_a], color='black', linewidth=3)
        plt.plot([M_a, M_b], [N_b, N_b], color='black', linewidth=3)
        for m in range (M+1):
            #plt.plot([m_division_array[m], m_division_array[m]], [0, N], color='grey', linestyle='--')
            plt.plot([m_division_array[m], m_division_array[m]], [0, N], color='grey')
        for n in range (N+1):
            #plt.plot([0, M], [n_division_array[n], n_division_array[n]], color='grey', linestyle='--')
            plt.plot([0, M], [n_division_array[n], n_division_array[n]], color='grey')
        plt.title('Malha')
        plt.show()