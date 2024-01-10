from inputs import *
from functions import *

# aqui precisamos do csv correto com todos os dados que vamos precisar
# adicionar mais cálculos, Vmax e Vmin

def get_polar():
    alpha_array = get_array_csv('alpha', 'clalphaaviao') # no segundo espaço botar csv correto
    #delta_array = get_array_csv('DELTA', 'dados') # delta é o ang. de deflexão do profundor

    # arrays
    cl_array = get_array_csv('CL', 'clalphaaviao') # no segundo espaço botar csv correto
    cd_array = get_array_csv('CD', 'clalphaaviao') # no segundo espaço botar csv correto
    cm_array = get_array_csv('Cm', 'clalphaaviao') # no segundo espaço botar csv correto

    # polyfits
    cl_alpha_coeff = get_coeff(alpha_array, cl_array, 1)
    cd_alpha_coeff = get_coeff(alpha_array, cd_array, 2)
    cm_alpha_coeff = get_coeff(alpha_array, cm_array, 1)

    cl_cd_coeff = get_coeff(cl_array, cd_array, 2)
    # print(cl_cd_coeff)

    # Arrays
    total_cl_array = []
    total_cd_array = []
    total_cm_array = []

#   get_plot(cl_array, cd_array, 'Cl', 'Cd', 'Polar de Arrasto')
#   plt.show()
#   
#   get_plot(cd_array, cl_array, 'Cd', 'Cl', 'Cl x Cd')
#   plt.show()

    return cl_cd_coeff, cl_array, alpha_array
