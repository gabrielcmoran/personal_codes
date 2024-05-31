import os
import subprocess
import matplotlib.pyplot as plt
import numpy as np
from avl_routines import Config_change as config

def run_avl(output_type,output_file="result.txt"):
    dir_name = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.join(dir_name, 'test.avl')
    run_case_file = os.path.join(dir_name, 'trim_test.run')
    outputs_path = os.path.join(dir_name, 'outputs')
    avl_path = os.path.join(dir_name, 'avl.exe')  # Assuming avl.exe is in the same directory as the script
    comm_string = f'load {config_file}\n case {run_case_file}\n oper\n x\n {output_type}\n{output_file}\n'
    Process = subprocess.Popen([avl_path],stdin=subprocess.PIPE, shell=True)
    Process.communicate(bytes(comm_string, encoding='utf8'))

def set_parameters():
    dir_name = os.path.dirname(os.path.abspath(__file__))
    avl_path = os.path.join(dir_name, 'avl.exe')  # Assuming avl.exe is in the same directory as the script
    comm_string = f''
    Process = subprocess.Popen([avl_path], stdin=subprocess.PIPE, shell=True)
    Process.communicate(bytes(comm_string, encoding='utf8'))
def run_avl_alpha(alpha, velocity, file_path, is_flapped=False):
    '''Runs the configuration file on AVL for an especified alpha,
    both AVL and the configuration file need to be in the same directory'''
    dir_name = os.path.dirname(os.path.abspath(__file__))
    config_file = file_path
    output_file = f'result{alpha}.txt'
    output_file_path = os.path.join(dir_name, output_file)
    avl_path = os.path.join(dir_name, 'avl.exe')  # Assuming avl.exe is in the same directory as the script
    if is_flapped:
        comm_string = f'load {config_file}\noper\nm\nv {velocity}\ng 9.8\nd 1.225\n\na a {alpha}\nd1 d1 15\nx\nft\n{output_file_path}\n'
    else:
        comm_string = f'load {config_file}\noper\nm\nv {velocity}\ng 9.8\nd 1.225\n\na a {alpha}\nx\nft\n{output_file_path}\n'
    Process = subprocess.Popen([avl_path], stderr= subprocess.PIPE, stdout=subprocess.PIPE ,stdin=subprocess.PIPE, shell=True)
    Process.communicate(bytes(comm_string, encoding='utf8'))
    return output_file_path

def read_var_value(file,var):
    '''Reads the variable value from the designated file,
    which has to be an "Total Forces Analisys" output from AVL'''
    with open(file, 'r') as file_aux:
        lines = file_aux.readlines()
        if var == 'CL':
            line = lines[23]
            value = line[11:19]
            return value
        if var == 'CM':
            line = lines[20]
            value = line[31:41]
            return value
        if var == 'CD':
            line = lines[24]
            value = line[11:19]
            return value

def plot_graph(x_axis,y_axis,xname,yname,title):
    '''Function used to make plotting easier inside other funtions'''
    plt.plot(x_axis, y_axis)
    plt.xlabel(f'{xname}')
    plt.ylabel(f'{yname}')
    plt.title(f'{title}')
    plt.grid(True, linestyle='--')
    plt.show()

def run_alpha_range(file_path, start_alpha=-15,finish_alpha=15,pace=1):
    alphas = [i * pace for i in range(int(start_alpha/pace), int(finish_alpha/pace)+1)]
    #Generates a list of alphas with the desired start, finish and pace
    cl_list = []
    cm_list = []
    cd_list = []

    for alpha in alphas:
        file_to_read = run_avl_alpha(alpha,10, file_path)
        dir_name = os.path.dirname(os.path.abspath(__file__))
#        file_to_read = os.path.join(dir_name, f'result{alpha}.txt')
        cd = float(read_var_value(file_to_read,'CD'))
        cl = float(read_var_value(file_to_read,'CL'))
        cm = float(read_var_value(file_to_read,'CM'))
        cl_list.append(cl)
        cm_list.append(cm)
        cd_list.append(cd)

        os.remove(file_to_read)

    return alphas, cl_list, cm_list, cd_list

def get_angular_coeffs(file_path):
    alphas, cl, cm, cd = run_alpha_range(file_path,-2,2)
    np_alphas = np.array(alphas)
    np_cl = np.array(cl)
    np_cm = np.array(cm)
    np_cd = np.array(cd)
    cl_a = np.polyfit(np_alphas, np_cl,1)
    cm_a = np.polyfit(np_alphas, np_cm,1)
    cd_a = np.polyfit(np_alphas, np_cd,1)
    return cl_a, cm_a, cd_a



'''
alphas, cl_list, cm_list, cd_list = run_alpha_range(-5,20)
print("Alphas")
print(alphas)
print("CL")
print(cl_list)
print("CM")
print(cm_list)
print("CD")
print(cd_list)
plot_graph(alphas,cl_list,'Alpha','Cl','Cl x Alpha')
plot_graph(alphas,cm_list,'Alpha','Cm','Cm x Alpha')
plot_graph(alphas,cd_list,'Alpha','Cd','Cd x Alpha')


#run_avl('st','resultST.txt')
#read_NP(ST_file)
'''