import matplotlib.pyplot as plt

def spacial_discretization(M,N,M_a,N_a,N_b,delta_x_a,delta_x_b,delta_y_a,delta_y_b,delta_y_c,plot):
    x_array = []
    y_array = []
    for m in range (M+1):
        print(m)
        for n in range(N+1):
            if m <= M_a:
                x_position = m*delta_x_a*10**3
            elif m > M_a:
                x_position = (M_a*delta_x_a + (m-M_a)*delta_x_b)*10**3
            if n <= N_a:
                y_position = n*delta_y_a*10**3
            elif N_a < n <= N_b:
                y_position = (N_a*delta_y_a + (n-N_a)*delta_y_b)*10**3
            elif n > N_b:
                y_position = (N_a*delta_y_a + (N_b - N_a)*delta_y_b + (n-N_b)*delta_y_c)*10**3
            
            x_array.append(x_position)
            y_array.append(y_position)
    
    if plot == 1:
        plt.scatter(x_array, y_array)
        plt.xlabel('Eixo X')
        plt.ylabel('Eixo Y')
        plt.title('Gráfico de Pontos')
        plt.plot([5, 5], [8, 16], color='blue')
        plt.plot([5, 10], [8, 8], color='blue')
        plt.plot([5, 10], [16, 16], color='blue')
        plt.show()