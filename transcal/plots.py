import matplotlib.pyplot as plt
import matplotlib.patches as patches
import imageio.v2 as imageio
import numpy as np

def spacial_discretization(M,N,M_a,M_b,N_a,N_b,delta_x,delta_y):
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
        
    fig, ax = plt.subplots()
    ax.tick_params(axis='both', which='major', labelsize=12)
    background_rect = patches.Rectangle((0, 0), M, N, linewidth=0, edgecolor='none', facecolor='#D3D3D3')
    ax.add_patch(background_rect)
    rect = patches.Rectangle((M_a, N_a), (M - M_a), (N_b - N_a), linewidth=1, edgecolor='black', facecolor='#ADD8E6')
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
        plt.plot([m_division_array[m], m_division_array[m]], [0, N], color='grey')
    for n in range (N+1):
        plt.plot([0, M], [n_division_array[n], n_division_array[n]], color='grey')
    plt.title('Malha')
    plt.savefig('mesh.png', bbox_inches='tight')
    plt.show()

def plot_Q_dot_ratio(time_array,Q_dot_ratio_array,time_needed_PR):
    print(f'Tempo para atingir regime permanente: {time_needed_PR}')
    plt.plot(time_array, Q_dot_ratio_array)
    plt.xlabel('Tempo [s]')
    plt.ylabel('Razão')
    plt.title('Razão entre as taxas de transferência de calor')
    plt.savefig('ratio.png', bbox_inches='tight')
    plt.savefig('Q_dot_ratio.png', bbox_inches='tight')
    plt.show()

def evalueted_knots_temperature(time_array,A_knot_temperature,B_knot_temperature,C_knot_temperature,D_knot_temperature):
    plt.plot(time_array, A_knot_temperature, label='Nó A')
    plt.plot(time_array, B_knot_temperature, label='Nó B')
    plt.plot(time_array, C_knot_temperature, label='Nó C')
    plt.plot(time_array, D_knot_temperature, label='Nó D')
    plt.xlabel('Tempo [s]')
    plt.ylabel('Temperatura [°C]')
    plt.title('Temperatura dos nós avaliados')
    plt.legend()
    plt.savefig('evalueted_knots.png', bbox_inches='tight')
    plt.show()

def generate_temperature_plot(T,i,M):
    T_matrix = T[i]
    T_matrix = T_matrix - 273
    T_matrix = T_matrix[:, ::-1]
    T_matrix = np.transpose(T_matrix)
    plt.imshow(T_matrix, cmap='hot', interpolation='nearest', vmin=15, vmax=33)
    cbar = plt.colorbar()
    cbar.set_label('Temperatura [°C]')
    plt.title("Distribuição de temperaturas")
    plt.yticks(np.arange(0, T_matrix.shape[0], 4), np.flip(np.arange(0, T_matrix.shape[0], 4)))
    plt.xticks(np.arange(0, M, 2))
    filename = f'images/figure_{i}.png'
    filenames.append(filename)
    plt.savefig(filename, bbox_inches='tight')
    plt.close()

filenames = []
def generate_temperature_gif(T,M):
    print('Criando GIF')
    for i in range(len(T)):
        generate_temperature_plot(T,i,M)
    with imageio.get_writer('temperature_gif.gif', fps=3) as writer:
        for filename in filenames:
            image = imageio.imread(filename)
            writer.append_data(image)
        image = imageio.imread(f'images/figure_38.png')
        writer.append_data(image)
    print('GIF criado')