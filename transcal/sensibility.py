from parameters import *
from system_of_equations import solving_system_of_equations
from plots import *

def sensibility_analysis(q_dot_0,h,T_inf,K,alpha):
    time_needed_PR_array = []
    q_dot_0_array = []
    h_array = []
    T_inf_array = []
    K_array = []
    alpha_array = []
    q_dot_0_new = 0.9*q_dot_0
    q_dot_0_increment = -0.02*q_dot_0
    h_new = 1.1*h
    h_increment = 0.02*h
    T_inf_new = T_inf - 10
    T_inf_increment = -2
    K_new = 1.1*K
    K_increment = 0.02*K
    alpha_new = 1.1*alpha
    alpha_increment = 0.02*alpha

    while h <= h_new:
        solving = solving_system_of_equations(M,N,q_dot_0,alpha,h,T_inf,K,delta_t)
        time_needed_PR = solving[7]
        time_needed_PR_array.append(time_needed_PR)
        h_array.append(h)
        h = h + h_increment
    return h_array,time_needed_PR_array

def plot_sensibility_analysis(property_array,time_needed_PR_array):
    # T_inf change
    #property_array = [property_array[i]-273 for i in range(len(property_array))]
    #plt.plot(property_array, time_needed_PR_array)
    #plt.xlabel('Temperatura da água [°C]')
    #plt.ylabel('Tempo até atingir regime permanente [s]')
    #plt.title('Alteração na temperatura da água')
    #plt.savefig('temp_water.png', bbox_inches='tight')
    #plt.show()

    # q_dot_0 change
    #plt.plot(property_array, time_needed_PR_array)
    #plt.xlabel('Fluxo de calor dissipado pelo chip [W/m²]')
    #plt.ylabel('Tempo até atingir regime permanente [s]')
    #plt.title('Variação do calor dissipado pelo chip')
    #plt.savefig('heat_cheap.png', bbox_inches='tight')
    #plt.show()

    # h change
    plt.plot(property_array, time_needed_PR_array)
    plt.xlabel('Coeficiente de convecção com a água [W/m²K]')
    plt.ylabel('Tempo até atingir regime permanente [s]')
    plt.title('Variação do coeficiente de convecção')
    plt.savefig('h_change.png', bbox_inches='tight')
    plt.show()

    # K change
    #plt.plot(property_array, time_needed_PR_array)
    #plt.xlabel('Condutividade térmica [W/mK]')
    #plt.ylabel('Tempo até atingir regime permanente [s]')
    #plt.title('Variação da condutividade térmica')
    #plt.savefig('K_change.png', bbox_inches='tight')
    #plt.show()

    # alpha change
    #plt.plot(property_array, time_needed_PR_array)
    #plt.xlabel('Difusividade térmica [m²/s]')
    #plt.ylabel('Tempo até atingir regime permanente [s]')
    #plt.title('Variação da difusividade térmica')
    #plt.savefig('alpha_change.png', bbox_inches='tight')
    #plt.show()

sensibility_analysis = sensibility_analysis(q_dot_0,h,T_inf,K,alpha)
plot_sensibility_analysis(sensibility_analysis[0],sensibility_analysis[1])

