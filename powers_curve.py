from inputs import *
from functions import *
from drag_polar_plane import *

# verificar a polar e trocar a variavel cl_cd_coeff
# tem que ser a polar invertida (CdxCl)

plot = False
cl_cruise = 0.993134
displacement_x_max = 55 # maximum displacemenet before the first corner
delta_altitude_min = 10 # minimum altitude needed to obtain during the horizontal displacement before the first corner

def get_powers_curve(total_mass,gravity_acceleration,wing_area,air_density,air_density_0,cl_cd_coeff,cl_cruise,motor_static_thrust,motor_decay_coeff,load_factor_max,displacement_x_max,delta_altitude_min,plot):
    # Variables initialization
    velocity = 0.5 # [m/s]
    delta_velocity = 0.01 # speed variation during power curve analysis [m/s]
    total_weight = get_weight(total_mass, gravity_acceleration)
    deltaP_max = 0
    velocity_deltaP_max = 0
    cl_deltaP_max = 0
    rate_of_climb_max = -10**8
    velocity_rate_of_climb_max = 0
    required_thrust_min = 10**8
    velocity_required_thrust_min = 0
    cl_required_thrust_min = 0
    required_power_min = 10**8
    velocity_required_power_min = 0
    cl_required_power_min = 0
    required_power_required_thrust_min = 0
    available_thrust_required_thrust_min = 0
    available_power_required_thrust_min = 0
    available_thrust_required_power_min = 0
    available_power_required_power_min = 0
    deltaP = 0
    minimum_excess_power_needed = False

    # Arrays
    available_thrust_array = []
    required_thrust_array = []
    available_power_array = []
    required_power_array = []
    rate_of_climb_array = []
    velocity_array = []
    deltaP_array = []
    velocity_operation_array = []
    cl_array = []

    cl_cd_coeff = get_polar()[0]
    velocity_cruise = math.sqrt(2*total_weight/(wing_area*air_density*cl_cruise))
    cd_cruise = cl_cd_coeff[0]*(cl_cruise**2) + cl_cd_coeff[1]*cl_cruise + cl_cd_coeff[2]

    while velocity <= 25:
        velocity = velocity + delta_velocity
        available_thrust = get_available_thrust(motor_static_thrust, velocity, motor_decay_coeff, air_density, air_density_0)

        cl = get_cl(total_weight, wing_area,air_density,velocity)
        cd = 2*(cl_cd_coeff[0]*(cl**2) + cl_cd_coeff[1]*cl + cl_cd_coeff[2])

        cl_array.append(cl)

        required_thrust = get_required_thrust(total_weight, cl, cd)
        available_power = get_available_power(available_thrust, velocity)
        required_power = get_required_power(required_thrust, velocity)
        rate_of_climb = get_rate_of_climb(required_power, available_power, total_weight)
        deltaP = available_power - required_power

        available_thrust_array.append(available_thrust)
        required_thrust_array.append(required_thrust)
        available_power_array.append(available_power)
        required_power_array.append(required_power)
        rate_of_climb_array.append(rate_of_climb)
        velocity_array.append(velocity)
        deltaP_array.append(deltaP)

        if deltaP>0: # determining operating speeds
            velocity_operation_array.append(velocity)

        if deltaP>deltaP_max: # determining maximum excess power
            deltaP_max = deltaP
            velocity_deltaP_max = velocity
            cl_deltaP_max = cl
        
        if required_thrust<required_thrust_min: # determining minimum required thrust
            required_thrust_min = required_thrust
            velocity_required_thrust_min = velocity # maximum range speed
            cl_required_thrust_min = cl
            required_power_required_thrust_min = get_required_power(required_thrust_min,velocity_required_thrust_min)
            available_thrust_required_thrust_min = get_available_thrust(motor_static_thrust,velocity_required_thrust_min,motor_decay_coeff,air_density,air_density_0)
            available_power_required_thrust_min = get_available_power(available_thrust_required_thrust_min,velocity_required_thrust_min)
        
        if required_power<required_power_min: # determining minimum required mower
            required_power_min = required_power
            velocity_required_power_min = velocity # maximum autonomy speed
            cl_required_power_min = cl
            available_thrust_required_power_min = get_available_thrust(motor_static_thrust,velocity_required_power_min,motor_decay_coeff,air_density,air_density_0)
            available_power_required_power_min = get_available_power(available_thrust_required_power_min,velocity_required_power_min)
        if rate_of_climb > rate_of_climb_max:
            rate_of_climb_max = rate_of_climb
            velocity_rate_of_climb_max =  velocity
            minimum_rate_of_climb_max_needed = (delta_altitude_min/displacement_x_max)*velocity_rate_of_climb_max

    cl_stall = max(get_polar()[1])
    cd_stall = cl_cd_coeff[0]*(cl_stall**2) + cl_cd_coeff[1]*cl_stall + cl_cd_coeff[2]
    velocity_stall = math.sqrt(((2 * total_weight) / (wing_area * air_density * cl_stall)))
    available_thrust_stall = get_available_thrust(motor_static_thrust,velocity_stall,motor_decay_coeff,air_density,air_density_0)
    available_power_stall = get_available_power(available_thrust_stall,velocity_stall)
    required_thrust_stall = get_required_thrust(total_weight,cl_stall,cd_stall)
    required_power_stall = get_required_power(required_thrust_stall,velocity_stall)

    available_thrust_cruise = get_available_thrust(motor_static_thrust,velocity_cruise,motor_decay_coeff,air_density,air_density_0)
    available_power_cruise = get_available_power(available_thrust_cruise,velocity_cruise)
    required_thrust_cruise = get_required_thrust(total_weight,cl_cruise,cd_cruise)
    required_power_cruise = get_required_power(required_thrust_cruise,velocity_cruise)

    velocity_maneuver = velocity_stall*math.sqrt(load_factor_max)
    
    if velocity_operation_array == []:
        velocity_min = velocity_max = 0
    else:
        velocity_min = min(velocity_operation_array)
        velocity_max = max(velocity_operation_array)

    available_thrust_min = get_available_thrust(motor_static_thrust,velocity_min,motor_decay_coeff,air_density,air_density_0)
    available_power_min = get_available_power(available_thrust_min,velocity_min)

    available_thrust_max = get_available_thrust(motor_static_thrust,velocity_max,motor_decay_coeff,air_density,air_density_0)
    available_power_max = get_available_power(available_thrust_max,velocity_max)

    if rate_of_climb_max > minimum_rate_of_climb_max_needed:
        minimum_excess_power_needed = True

    print('Curvas de potência')
    print(f'V_min = {velocity_min:.2f}, V_max = {velocity_max:.2f}, V_stall = {velocity_stall:.2f}, V_cruise = {velocity_cruise:.2f}')
    print(f'R/C_max = {rate_of_climb_max:.2f}, V_R/C_max = {velocity_rate_of_climb_max:.2f}')

    if plot == True:
        plt.plot(velocity_array, available_power_array, label = 'Potência disponível')
        plt.plot(velocity_array, required_power_array, label = 'Potência requerida')

        plt.scatter(velocity_min, available_power_min, facecolors='none', edgecolors='green', marker='o', s=50, label='$V_{mínima}$')
        plt.scatter(velocity_max, available_power_max, facecolors='none', edgecolors='black', marker='o', s=50, label='$V_{máxima}$')
        plt.scatter(velocity_stall, available_power_stall, facecolors='none', edgecolors='red', marker='*', s=80, label='$V_{estol}$')
        plt.scatter(velocity_stall, required_power_stall, facecolors='none', edgecolors='red', marker='*', s=80)
        plt.scatter(velocity_required_thrust_min, required_power_required_thrust_min, facecolors='none', edgecolors='purple', marker='^', s=50, label='$V_{máximo\ alcance}$')
        plt.scatter(velocity_required_thrust_min, available_power_required_thrust_min, facecolors='none', edgecolors='purple', marker='^', s=50)
        plt.scatter(velocity_required_power_min, required_power_min, facecolors='none', edgecolors='blue', marker='s', s=50, label='$V_{máxima\ autonomia}$')
        plt.scatter(velocity_required_power_min, available_power_required_power_min, facecolors='none', edgecolors='blue', marker='s', s=50)
        plt.scatter(velocity_cruise, available_power_cruise, facecolors='none', edgecolors='orange', marker='d', s=50, label='$V_{cruzeiro}$')
        plt.scatter(velocity_cruise, required_power_cruise, facecolors='none', edgecolors='orange', marker='d', s=50)

        plt.plot([velocity_min, velocity_min], [0, available_power_min], linestyle='--', color='grey')
        plt.plot([velocity_max, velocity_max], [0, available_power_max], linestyle='--', color='grey')
        plt.plot([velocity_stall, velocity_stall], [0, available_power_stall], linestyle='--', color='grey')
        plt.plot([velocity_required_thrust_min, velocity_required_thrust_min], [0, available_power_required_thrust_min], linestyle='--', color='grey')
        plt.plot([velocity_required_power_min, velocity_required_power_min], [0, available_power_required_power_min], linestyle='--', color='grey')
        plt.plot([velocity_cruise, velocity_cruise], [0, available_power_cruise], linestyle='--', color='grey')

        plt.xlim(1, (velocity_max + 5))
        plt.ylim(0, (max(available_power_array)+50))
        plt.xlabel('$V_{\u221E} [m/s]$', fontsize=12)
        plt.ylabel('Potência [W]', fontsize=12)
        plt.title('Curvas de potência')

        plt.grid(True)
        plt.legend()
        plt.show()

        plt.plot(velocity_array, rate_of_climb_array)
        plt.xlim(velocity_min, velocity_max)
        plt.ylim(0,(1.2*rate_of_climb_max))
        plt.xlabel('$V_{\u221E} [m/s]$', fontsize=12)
        plt.ylabel('R/C [m/s]', fontsize=12)
        #plt.legend(True)
        plt.grid(True)
        plt.show()
    return (velocity_min,velocity_max,velocity_stall,velocity_cruise,velocity_maneuver,minimum_excess_power_needed)

cl_cd_coeff = get_polar()[0]
powers_curve = get_powers_curve(total_mass,gravity_acceleration,wing_area,air_density_sjdc,air_density_0,cl_cd_coeff,cl_cruise,motor_static_thrust,motor_decay_coeff,load_factor_max,displacement_x_max,delta_altitude_min,plot)