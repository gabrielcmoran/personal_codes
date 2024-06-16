import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

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
        #fig, ax = plt.subplots()
        #plt.xlim(0,10)
        #plt.ylim(int(0),int(20))
        #plt.plot([5, 5], [8, 16], color='black')
        #plt.plot([5, 10], [8, 8], color='black')
        #plt.plot([5, 10], [16, 16], color='black')
        #plt.plot([0, 10], [8, 8], color='grey', linestyle='--', label='Posição dos nós (m,$N_a$)')
        #plt.plot([0, 10], [16, 16], color='grey', linestyle='-.', label='Posição dos nós (m,$N_b$)')
        #plt.plot([5, 5], [0, 20], color='grey', linestyle=':', label='Posição dos nós ($M_a$,n)')
        #ax.tick_params(axis='both', which='major', labelsize=12)
        #background_rect = patches.Rectangle((0, 0), 10, 20, linewidth=0, edgecolor='none', facecolor='#D3D3D3')
        #ax.add_patch(background_rect)
        #rect = patches.Rectangle((5, 8), 5, 8, linewidth=1, edgecolor='black', facecolor='#ADD8E6')
        #ax.add_patch(rect)
        #plt.xlabel('Posição em x [mm]',fontsize=14)
        #plt.ylabel('Posição em y [mm]',fontsize=14)
        #plt.title('Seção representativa',fontsize=16)
        #plt.legend(loc='lower left',fontsize=10.5)
        #plt.show()
        
        fig, ax = plt.subplots()
        ax.tick_params(axis='both', which='major', labelsize=12)
        background_rect = patches.Rectangle((0, 0), 14, 20, linewidth=0, edgecolor='none', facecolor='#D3D3D3')
        ax.add_patch(background_rect)
        rect = patches.Rectangle((7, 8), 7, 8, linewidth=1, edgecolor='black', facecolor='#ADD8E6')
        ax.add_patch(rect)
        plt.scatter(m_array, n_array,s=50)
        plt.xlim(0,M)
        plt.ylim(0,N)
        plt.xlabel('m',fontsize='12')
        plt.ylabel('n',fontsize='12')
        ax.set_yticks(np.arange(0, N+1, 4))
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