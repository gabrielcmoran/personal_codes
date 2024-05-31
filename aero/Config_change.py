#Airplane Configuration
import os

def get_airfoil_file(data):
    dir_name = os.path.dirname(os.path.abspath(__file__))
    af_dir = os.path.join(dir_name, 'af')
    airfoil_path = os.path.join(af_dir, str(data) + '.dat')#be careful to use this function, the library can only handle paths with max 75 charachters
    return airfoil_path


def change_config(data, newfile_path):

    Wy1 = 0
    Wy2 = data.get('span_1th_to_2th_section')
    Wy3 = data.get('span_2th_to_3th_section') + Wy2
    Wc1 = data.get("chord_1th_section")
    Wc2 = data.get("chord_2th_section")
    Wc3 = data.get("chord_3th_section")
    Wa1 = get_airfoil_file(data.get("airfoil_name_1th_section"))
    Wa2 = get_airfoil_file(data.get("airfoil_name_2th_section"))
    Wa3 = get_airfoil_file(data.get("airfoil_name_3th_section"))
    Wa = data.get('incidence')

    MAC = float(((Wc1 + Wc2)*Wy2 + (Wc2 + Wc3)*Wy3)/((Wy2 + Wy3)*2))
    X_ac = round(MAC/4,4)

    C_ref = round(MAC,4)
    B_ref = (Wy2 + Wy3)*2
    S_ref = C_ref * B_ref

    dir_name = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(dir_name, 'placeholder.txt')

    with open(file_path, 'r') as file_aux:
        lines = file_aux.readlines()

        for i in range(len(lines)):
            if ('Sref') in lines[i]:
                index_refs = i
            elif ('Xref') in lines[i]:
                index_poscg = i
            elif lines[i] == ('SECTION!surface_start\n'):
                index_start = i + 1
            elif lines[i] == ('SECTION!surface_mid\n'):
                index_mid = i + 1
            elif lines[i] == ('SECTION!surface_end\n'):
                index_end = i + 1
            elif lines[i] == ('ANGLE!surface\n'):
                index_wa = i + 1
            elif lines[i] == ('AFIL!airfoil_start\n'):
                index_as = i + 1
            elif lines[i] == ('AFIL!airfoil_mid\n'):
                index_am = i + 1
            elif lines[i] == ('AFIL!airfoil_end\n'):
                index_ae = i + 1

        lines[index_poscg] = f'{X_ac} 0.0 0.0 !Xref   Yref   Zref   moment reference location (m)(arb.)\n'
        lines[index_refs] = f'{S_ref} {C_ref} {B_ref} !Sref   Cref   Bref   reference area, chord, span\n'

        lines[index_wa] = f'{Wa}\n'
        lines[index_start] = f"0.00 {Wy1} 0.0 {Wc1} 0.0\n"
        lines[index_mid] = f"0.00 {Wy2} 0.0 {Wc2} 0.0\n"
        lines[index_end] = f"0.00 {Wy2 + Wy3} 0.0 {Wc3} 0.0\n"

        lines[index_as] = f'{Wa1}\n'
        lines[index_am] = f'{Wa2}\n'
        lines[index_ae] = f'{Wa3}\n'


    with open(newfile_path, 'w') as file:
        text = ""
        for a in lines:
            text = text + a
        file.write(text)

'''def change_config_legacy(data):
    with open("C:/Users/luisf/Downloads/AVL/my_runs/test.avl", 'r') as file_aux:
        lines = file_aux.readlines()

        for i in range(len(lines)):
            if ('Xref') in lines[i]:
                index_poscg = i
            # =====Config Wing
            if lines[i] == ('SECTION!wing_start\n'):
                index_startwing = i + 1
            elif lines[i] == ('SECTION!wing_mid\n'):
                index_midwing = i + 1
            elif lines[i] == ('SECTION!wing_end\n'):
                index_endwing = i + 1
            elif lines[i] == ('ANGLE!wing\n'):
                index_awing = i + 1
            # =====Config EH
            elif lines[i] == ('SECTION!eh_start\n'):
                index_starteh = i + 1
            elif lines[i] == ('SECTION!eh_end\n'):
                index_endeh = i + 1
            elif lines[i] == ('TRANSLATE!eh\n'):
                index_poseh = i + 1
            elif lines[i] == ('ANGLE!eh\n'):
                index_aeh = i + 1
            #=====Config EV
            elif lines[i] == ('SECTION!ev_start\n'):
                index_startev = i + 1
            elif lines[i] == ('SECTION!ev_end\n'):
                index_endev = i + 1
            elif lines[i] == ('TRANSLATE!ev\n'):
                index_posev = i + 1
            elif lines[i] == ('ANGLE!ev\n'):
                index_aev = i + 1

        lines[index_poscg] = f'{X_cg} 0.0 0.0! Xref   Yref   Zref   moment reference location (m)(arb.)'

        lines[index_startwing] = f"0.00 {Wy1} 0.0 {Wc1} 0.0\n"
        lines[index_midwing] = f"0.00 {Wy2} 0.0 {Wc2} 0.0\n"
        lines[index_endwing] = f"0.00 {Wy3} 0.0 {Wc3} 0.0\n"
        lines[index_awing] = f"{Wa}\n"

        lines[index_starteh] = f"0.00 {Hy1} 0.0 {Hc1} 0.0\n"
        lines[index_endeh] = f"0.00 {Hy2} 0.0 {Hc2} 0.0\n"
        lines[index_poseh] = f"{X_eh} {Y_eh} {Z_eh}\n"
        lines[index_aeh] = f"{Ha}\n"

        lines[index_startev] = f"0.00 0.0 {Vz1} {Vc1} 0.0\n"
        lines[index_endev] = f"0.00 0.0 {Vz2} {Vc2} 0.0\n"
        lines[index_poseh] = f"{X_ev} {Y_ev} {Z_ev}\n"
        lines[index_aeh] = f"{Va}\n"

    with open("C:/Users/luisf/Downloads/AVL/my_runs/test2.avl", 'w') as file:
        text = ""
        for a in lines:
            text = text + a
        print(file)
        file.write(text)
'''