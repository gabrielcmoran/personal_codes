import math
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.interpolate import interp1d

#           car data
# inertia
car_mass = 1580 # [kg]
fuel_density = 715  # [kg/m³]
fuel_volume = 63 # [l]
fuel_mass = fuel_density*(fuel_volume/1000) # [kg]
driver_mass = 80 # [kg]
car_total_mass = car_mass + fuel_mass + driver_mass # [kg]
car_total_weight = car_total_mass*9.81 # [N]
#rotational_inertia_0_degree_coeff = 0.004
#rotational_inertia_2_degree_coeff = 0.05
rotational_inertia_0_degree_coeff = 0.15
rotational_inertia_2_degree_coeff = 0.001

# aerodynamics
air_density = 1.225 # [kg/m³]
drag_area_coeff = 0.684 # [m²]

# tires
widht_front_tire = 245 # [mm]
widht_rear_tire = 265 # [mm]
height_to_widht_ratio = 40*0.01 # [-]
rim_diameter = 18 # [pol]
slip_coeff = 0.02 # [-]
front_tire_external_diameter = 2*height_to_widht_ratio*widht_front_tire + rim_diameter*25.4 # [mm]
rear_tire_external_diameter = 2*height_to_widht_ratio*widht_rear_tire + rim_diameter*25.4 # [mm]
front_tire_static_radius = 0.47*front_tire_external_diameter # [mm]
rear_tire_static_radius = 0.47*rear_tire_external_diameter # [mm]
front_tire_dinamic_radius = 1.02*front_tire_static_radius # [mm]
rear_tire_dinamic_radius = 1.02*rear_tire_static_radius # [mm]
rolling_friction_0_degree = 0.015
rolling_friction_2_degree = 0.052


# transmission
gear_ratio_1st_gear = 4.78 # [:1]
gear_ratio_2st_gear = 2.933 # [:1]
gear_ratio_3st_gear = 2.153 # [:1]
gear_ratio_4st_gear = 1.678 # [:1]
gear_ratio_5st_gear = 1.39 # [:1]
gear_ratio_6st_gear = 1.203 # [:1]
gear_ratio_7st_gear = 1 # [:1]
final_drive_ratio = 3.154 # [:1]
mechanical_performance = 0.85

# engine
engine_rotation_cut = 8400 # [rpm]
engine_minimum_rotation = 1150 # [rpm]
dataframe1 = pd.read_csv('torque.csv')
rotation_torque_array = dataframe1['omega'].tolist()
engine_torque_array = dataframe1['torque'].tolist()
dataframe2 = pd.read_csv('potencia.csv')
rotation_power_array = dataframe2['omega'].tolist()
engine_power_array = [0.7457 * value for value in dataframe2['power'].tolist()] # [kW]
#engine_power_array = [745.7 * value for value in dataframe2['power'].tolist()] # [W]
#engine_power_array = dataframe2['power'].tolist() # [hp]


# speed diagram
gear_ratio_array = [gear_ratio_1st_gear,gear_ratio_2st_gear,gear_ratio_3st_gear,gear_ratio_4st_gear,gear_ratio_5st_gear,gear_ratio_6st_gear,gear_ratio_7st_gear]
gear_index = 0
engine_rotation_array = []
speed_array = []

for gear_index in range(len(gear_ratio_array)):
    engine_rotation = engine_minimum_rotation
    gear_ratio = gear_ratio_array[gear_index]
    engine_rotaton_in_gear_array = []
    speed_in_gear_array = []
    while engine_rotation <= engine_rotation_cut:
        wheel_rotation_speed = (2*math.pi/60)*(engine_rotation/(gear_ratio*final_drive_ratio))
        tire_tangencial_speed = wheel_rotation_speed*((front_tire_dinamic_radius+rear_tire_dinamic_radius)/2)*10**-3
        car_speed = 3.6*tire_tangencial_speed*(1 - slip_coeff)
        engine_rotaton_in_gear_array.append(engine_rotation)
        speed_in_gear_array.append(car_speed)
        engine_rotation = engine_rotation + 50
    speed_array.append(speed_in_gear_array)
    engine_rotation_array.append(engine_rotaton_in_gear_array)
plot_a = 2
if plot_a == 1:
    plt.plot(engine_rotation_array[0], speed_array[0], label='Primeira marcha')
    plt.plot(engine_rotation_array[1], speed_array[1], label='Segunda marcha')
    plt.plot(engine_rotation_array[2], speed_array[2], label='Terceira marcha')
    plt.plot(engine_rotation_array[3], speed_array[3], label='Quarta marcha')
    plt.plot(engine_rotation_array[4], speed_array[4], label='Quinta marcha')
    plt.plot(engine_rotation_array[5], speed_array[5], label='Sexta marcha')
    plt.plot(engine_rotation_array[6], speed_array[6], label='Sétima marcha')
    plt.title('Diagrama de velocidades')
    plt.xlabel('Rotação do motor [rpm]')
    plt.ylabel('Velocidade do carro [km/h]')
    plt.legend()
    plt.grid()
    plt.show()


# engine curves
plot_b = 2
if plot_b == 1:
    fig, ax1 = plt.subplots()
    ax1.plot(rotation_torque_array, engine_torque_array, label = 'Torque', color = '#ff7f0e')
    ax1.set_xlabel('Rotação [rpm]')
    ax1.set_ylabel('Torque [Nm]', color='#ff7f0e')
    ax2 = ax1.twinx()
    ax2.plot(rotation_power_array, engine_power_array, label = 'Potência', color='#1f77b4')
    ax2.set_ylabel('Potência [kW]', color='#1f77b4')
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
    plt.grid()
    plt.show()
    

# car performance curves
gear_index = 0
power_in_cube_array = []
car_speed_array = []
consumed_power_array = []
car_maximum_speed = 0
car_maximum_power_in_cube = 0
total_consumed_power_0 = 0
car_speed_consumed_power_array = []
liquid_power_array = []
maximum_speed_at_gear = 0
maximum_speed_at_gear_array = []
minimum_speed_at_gear_array = []
maximum_acceleration_at_gear_array = []
maximum_slope_angle_at_gear_array = []
liquid_power_at_gear = 1
maximum_speed_reached = False
car_acceleration_array = []
slope_angle_array = []

for gear_index in range(len(gear_ratio_array)):
#for gear_index in range(1):
    maximum_acceleration_at_gear = 0
    maximum_slope_angle_at_gear = 0
    minimum_speed_reached = True
    gear_ratio = gear_ratio_array[gear_index]
    #rotational_inertia = rotational_inertia_0_degree_coeff + rotational_inertia_2_degree_coeff*(gear_ratio**2)
    rotational_inertia = rotational_inertia_0_degree_coeff + rotational_inertia_2_degree_coeff*((gear_ratio*final_drive_ratio)**2)
    #print(f': g_r: {gear_ratio:.2f}, r_in: {rotational_inertia:.2f}')
    engine_rotation = engine_minimum_rotation
    power_in_cube_at_gear_array = []
    car_speed_at_gear_array = []
    liquid_power_at_gear_array = []
    car_acceleration_at_gear_array = []
    slope_angle_at_gear_array = []

    while engine_rotation <= engine_rotation_cut:
        wheel_rotation_speed = (2*math.pi/60)*(engine_rotation/(gear_ratio*final_drive_ratio))
        tire_tangencial_speed = wheel_rotation_speed*(rear_tire_dinamic_radius*10**-3)
        car_speed = 3.6*tire_tangencial_speed*(1 - slip_coeff)
        power_in_cube_at_rotation = mechanical_performance*np.interp(engine_rotation, rotation_power_array, engine_power_array)

        if engine_rotation == engine_rotation_cut and liquid_power_at_gear > 0:
            maximum_speed_at_gear = car_speed
            maximum_speed_at_gear_array.append(maximum_speed_at_gear)

        rolling_friction_coeff = rolling_friction_0_degree + rolling_friction_2_degree*(car_speed/(3.6*100))**2
        rolling_consumed_power = rolling_friction_coeff*car_total_weight*tire_tangencial_speed
        drag_consumed_power = 0.5*air_density*drag_area_coeff*((car_speed/3.6)**3)
        total_consumed_power = (rolling_consumed_power + drag_consumed_power)/1000

        liquid_power_at_gear = power_in_cube_at_rotation - total_consumed_power
        car_acceleration_at_gear = (liquid_power_at_gear*1000/(car_speed/3.6))*(1 - slip_coeff)/(car_total_mass*(1 + rotational_inertia))
        car_acceleration_at_gear_array.append(car_acceleration_at_gear)

        slope_angle = math.asin(((liquid_power_at_gear*1000)/(car_speed/3.6))*(1-slip_coeff)/car_total_weight)
        slope_angle = math.degrees(slope_angle)

        if car_speed > maximum_speed_at_gear:
            car_speed_consumed_power_array.append(car_speed)
            consumed_power_array.append(total_consumed_power)
        
        if car_acceleration_at_gear > maximum_acceleration_at_gear:
            maximum_acceleration_at_gear = car_acceleration_at_gear
            
        if liquid_power_at_gear < 0 and not maximum_speed_reached:
            maximum_speed_at_gear = car_speed
            maximum_speed_at_gear_array.append(maximum_speed_at_gear)
            maximum_speed_reached = True
        
        if slope_angle > maximum_slope_angle_at_gear:
            maximum_slope_angle_at_gear = slope_angle
        
        if minimum_speed_reached:
            minimum_speed_at_gear = car_speed
            minimum_speed_reached = False

        car_speed_at_gear_array.append(car_speed)
        power_in_cube_at_gear_array.append(power_in_cube_at_rotation)
        liquid_power_at_gear_array.append(liquid_power_at_gear)
        slope_angle_at_gear_array.append(slope_angle)
        
        engine_rotation = engine_rotation + 50

        if car_speed > car_maximum_speed:
            car_maximum_speed = car_speed
        if power_in_cube_at_rotation > car_maximum_power_in_cube:
            car_maximum_power_in_cube = power_in_cube_at_rotation

    car_speed_array.append(car_speed_at_gear_array)
    power_in_cube_array.append(power_in_cube_at_gear_array)
    liquid_power_array.append(liquid_power_at_gear_array)
    car_acceleration_array.append(car_acceleration_at_gear_array)
    maximum_acceleration_at_gear_array.append(maximum_acceleration_at_gear)
    slope_angle_array.append(slope_angle_at_gear_array)
    maximum_slope_angle_at_gear_array.append(maximum_slope_angle_at_gear)
    minimum_speed_at_gear_array.append(minimum_speed_at_gear)


# time to change speed
delta_time = 0.1
time = 0
car_displacement = 0
car_speed = minimum_speed_at_gear_array[0]
car_speed_array_acc = []
time_array = []
car_displacement_array = []
reached_60_km_h = False
reached_80_km_h = False
reached_100_km_h = False
reached_120_km_h = False

for gear_index in range(len(gear_ratio_array)):
    while car_speed <= maximum_speed_at_gear_array[gear_index]:
        interpolation = interp1d(car_speed_array[gear_index], car_acceleration_array[gear_index], kind='linear', fill_value="extrapolate")
        car_acceleration = interpolation(car_speed)
        car_displacement = car_displacement + (car_speed/3.6)*delta_time + 0.5*car_acceleration*(delta_time**2)
        car_speed = car_speed + 3.6*car_acceleration*delta_time

        if car_speed >= 60 and not reached_60_km_h:
            time_to_60_km_h = time
            car_displacement_to_60_km_h = car_displacement
            reached_60_km_h = True
        
        if car_speed >= 80 and not reached_80_km_h:
            time_to_80_km_h = time
            car_displacement_to_80_km_h = car_displacement
            reached_80_km_h = True
        
        if car_speed >= 100 and not reached_100_km_h:
            time_to_100_km_h = time
            car_displacement_to_100_km_h = car_displacement
            reached_100_km_h = True
        
        if car_speed >= 120 and not reached_120_km_h:
            time_to_120_km_h = time
            car_displacement_to_120_km_h = car_displacement
            reached_120_km_h = True

        if car_acceleration <= 0.01:
            break
        
        time = time + delta_time
        car_speed_array_acc.append(car_speed)
        time_array.append(time)
        car_displacement_array.append(car_displacement)

# time to overtake (60 - 120 km/h)
delta_time = 0.1
car_speed_array_ovt = []
time_array_ovt = []
car_displacement_array_ovt = []
for gear_index in range(len(gear_ratio_array)):
#for gear_index in range(3):
    time = 0
    car_displacement = 0
    car_speed = 60
    car_speed_at_gear_array_ovt = []
    time_at_gear_array = []
    car_displacement_at_gear_array = []
    gear_index2 = gear_index
    #print(f't: {time:.2f}, g_i: {gear_index:.2f}')

    while gear_index2 <= len(gear_ratio_array):
    #while gear_index2 <= 3:
        if car_speed >= 120:
            break
        while car_speed <= maximum_speed_at_gear_array[gear_index2]:
            interpolation = interp1d(car_speed_array[gear_index2], car_acceleration_array[gear_index2], kind='linear', fill_value="extrapolate")
            car_acceleration = interpolation(car_speed)
            car_displacement = car_displacement + (car_speed/3.6)*delta_time + 0.5*car_acceleration*(delta_time**2)
            car_speed = car_speed + 3.6*car_acceleration*delta_time
            #print(f'a: {car_acceleration:.2f}, v: {car_speed:.2f}, g_i: {gear_index2}')

            if car_speed >= 120:
                break
            
            time = time + delta_time
            car_speed_at_gear_array_ovt.append(car_speed)
            time_at_gear_array.append(time)
            car_displacement_at_gear_array.append(car_displacement)
        gear_index2 = gear_index2 + 1
    
    car_speed_array_ovt.append(car_speed_at_gear_array_ovt)
    time_array_ovt.append(time_at_gear_array)
    car_displacement_array_ovt.append(car_displacement_at_gear_array)

plot_c = 2
if plot_c == 1:
    print('     Velocidades máximas em cada marcha:')
    print(f'Primeira marcha: {maximum_speed_at_gear_array[0]:.2f} km/h')
    print(f'Segunda marcha: {maximum_speed_at_gear_array[1]:.2f} km/h')
    print(f'Terceira marcha: {maximum_speed_at_gear_array[2]:.2f} km/h')
    print(f'Quarta marcha: {maximum_speed_at_gear_array[3]:.2f} km/h')
    print(f'Quinta marcha: {maximum_speed_at_gear_array[4]:.2f} km/h')
    print(f'Sexta marcha: {maximum_speed_at_gear_array[5]:.2f} km/h')
    print(f'Sétima marcha: {maximum_speed_at_gear_array[6]:.2f} km/h')
    print('     Velocidades mínimas em cada marcha:')
    print(f'Primeira marcha: {minimum_speed_at_gear_array[0]:.2f} km/h')
    print(f'Segunda marcha: {minimum_speed_at_gear_array[1]:.2f} km/h')
    print(f'Terceira marcha: {minimum_speed_at_gear_array[2]:.2f} km/h')
    print(f'Quarta marcha: {minimum_speed_at_gear_array[3]:.2f} km/h')
    print(f'Quinta marcha: {minimum_speed_at_gear_array[4]:.2f} km/h')
    print(f'Sexta marcha: {minimum_speed_at_gear_array[5]:.2f} km/h')
    print(f'Sétima marcha: {minimum_speed_at_gear_array[6]:.2f} km/h')
    print('-----------------')
    print('     Acelerações máximas em cada marcha:')
    print(f'Primeira marcha: {maximum_acceleration_at_gear_array[0]:.2f} m/s²')
    print(f'Segunda marcha: {maximum_acceleration_at_gear_array[1]:.2f} m/s²')
    print(f'Terceira marcha: {maximum_acceleration_at_gear_array[2]:.2f} m/s²')
    print(f'Quarta marcha: {maximum_acceleration_at_gear_array[3]:.2f} m/s²')
    print(f'Quinta marcha: {maximum_acceleration_at_gear_array[4]:.2f} m/s²')
    print(f'Sexta marcha: {maximum_acceleration_at_gear_array[5]:.2f} m/s²')
    print(f'Sétima marcha: {maximum_acceleration_at_gear_array[6]:.2f} m/s²')
    plt.plot(car_speed_array[0], power_in_cube_array[0], label='Primeira marcha')
    plt.plot(car_speed_array[1], power_in_cube_array[1], label='Segunda marcha')
    plt.plot(car_speed_array[2], power_in_cube_array[2], label='Terceira marcha')
    plt.plot(car_speed_array[3], power_in_cube_array[3], label='Quarta marcha')
    plt.plot(car_speed_array[4], power_in_cube_array[4], label='Quinta marcha')
    plt.plot(car_speed_array[5], power_in_cube_array[5], label='Sexta marcha')
    plt.plot(car_speed_array[6], power_in_cube_array[6], label='Sétima marcha')
    plt.plot(car_speed_consumed_power_array, consumed_power_array, label='Potência consumida')
    plt.xlabel('Velocidade [km/h]')
    plt.ylabel('Potência no cubo [kW]')
    plt.xlim(0,car_maximum_speed + 10)
    plt.ylim(0,car_maximum_power_in_cube + 10)
    plt.legend()
    plt.grid()
    plt.show()

plot_d = 2
if plot_d == 1:
    plt.plot(car_speed_array[0], liquid_power_array[0], label='Primeira marcha')
    plt.plot(car_speed_array[1], liquid_power_array[1], label='Segunda marcha')
    plt.plot(car_speed_array[2], liquid_power_array[2], label='Terceira marcha')
    plt.plot(car_speed_array[3], liquid_power_array[3], label='Quarta marcha')
    plt.plot(car_speed_array[4], liquid_power_array[4], label='Quinta marcha')
    plt.plot(car_speed_array[5], liquid_power_array[5], label='Sexta marcha')
    plt.plot(car_speed_array[6], liquid_power_array[6], label='Sétima marcha')
    plt.xlabel('Velocidade [km/h]')
    plt.ylabel('Potência líquida [kW]')
    plt.xlim(0,car_maximum_speed + 10)
    plt.ylim(0,car_maximum_power_in_cube + 10)
    plt.legend()
    plt.grid()
    plt.show()

plot_e = 2
if plot_e == 1:
    plt.plot(car_speed_array[0], car_acceleration_array[0], label='Primeira marcha')
    plt.plot(car_speed_array[1], car_acceleration_array[1], label='Segunda marcha')
    plt.plot(car_speed_array[2], car_acceleration_array[2], label='Terceira marcha')
    plt.plot(car_speed_array[3], car_acceleration_array[3], label='Quarta marcha')
    plt.plot(car_speed_array[4], car_acceleration_array[4], label='Quinta marcha')
    plt.plot(car_speed_array[5], car_acceleration_array[5], label='Sexta marcha')
    plt.plot(car_speed_array[6], car_acceleration_array[6], label='Sétima marcha')
    plt.xlabel('Velocidade [km/h]')
    plt.ylabel('Aceleração [m/s²]')
    plt.xlim(0,car_maximum_speed + 10)
    plt.ylim(0,maximum_acceleration_at_gear_array[0] + 0.2)
    plt.legend()
    plt.grid()
    plt.show()

plot_f = 2
if plot_f == 1:
    print('     Aclives máximos em cada marcha:')
    print(f'Primeira marcha: {maximum_slope_angle_at_gear_array[0]:.2f}°')
    print(f'Segunda marcha: {maximum_slope_angle_at_gear_array[1]:.2f}°')
    print(f'Terceira marcha: {maximum_slope_angle_at_gear_array[2]:.2f}°')
    print(f'Quarta marcha: {maximum_slope_angle_at_gear_array[3]:.2f}°')
    print(f'Quinta marcha: {maximum_slope_angle_at_gear_array[4]:.2f}°')
    print(f'Sexta marcha: {maximum_slope_angle_at_gear_array[5]:.2f}°')
    print(f'Sétima marcha: {maximum_slope_angle_at_gear_array[6]:.2f}°')
    plt.plot(car_speed_array[0], slope_angle_array[0], label='Primeira marcha')
    plt.plot(car_speed_array[1], slope_angle_array[1], label='Segunda marcha')
    plt.plot(car_speed_array[2], slope_angle_array[2], label='Terceira marcha')
    plt.plot(car_speed_array[3], slope_angle_array[3], label='Quarta marcha')
    plt.plot(car_speed_array[4], slope_angle_array[4], label='Quinta marcha')
    plt.plot(car_speed_array[5], slope_angle_array[5], label='Sexta marcha')
    plt.plot(car_speed_array[6], slope_angle_array[6], label='Sétima marcha')
    plt.xlabel('Velocidade [km/h]')
    plt.ylabel('Ângulo de aclive [°]')
    plt.xlim(0,car_maximum_speed + 10)
    plt.ylim(0,maximum_slope_angle_at_gear_array[0] + 5)
    plt.legend()
    plt.grid()
    plt.show()

plot_g = 2
if plot_g == 1:
    #print('----- Até 60 km/h: -----')
    #print(f'Tempo: {time_to_60_km_h:.2f} s')
    #print(f'Deslocamento: {car_displacement_to_60_km_h:.2f} m')
    #print('----- Até 80 km/h: -----')
    #print(f'Tempo: {time_to_80_km_h:.2f} s')
    #print(f'Deslocamento: {car_displacement_to_80_km_h:.2f} m')
    #print('----- Até 100 km/h: -----')
    #print(f'Tempo: {time_to_100_km_h:.2f} s')
    #print(f'Deslocamento: {car_displacement_to_100_km_h:.2f} m')
    #print('----- Até 120 km/h: -----')
    #print(f'Tempo: {time_to_120_km_h:.2f} s')
    #print(f'Deslocamento: {car_displacement_to_120_km_h:.2f} m')
    print('----- De 60 km/h a 120 km/h: -----')
    print(f'Tempo: {(time_to_120_km_h - time_to_60_km_h):.2f} s')
    print(f'Deslocamento: {(car_displacement_to_120_km_h - car_displacement_to_60_km_h):.2f} m')
    plt.plot(time_array, car_speed_array_acc)
    plt.xlabel('Tempo [s]')
    plt.ylabel('Velocidade [km/h]')
    plt.xlim(0,max(time_array))
    plt.ylim(0,max(car_speed_array_acc)+10)
    plt.grid()
    plt.show()

    plt.plot(time_array, car_displacement_array)
    plt.xlabel('Tempo [s]')
    plt.ylabel('Deslocamento [m]')
    plt.xlim(0,max(time_array))
    plt.ylim(0,max(car_displacement_array)+100)
    plt.grid()
    plt.show()

plot_h = 1
if plot_h == 1:
    print('----- Tempo de 60 km/h a 120 km/h -----')
    print(f'Primeira + segunda + terceira marchas: {max(time_array_ovt[0]):.2f} s')
    print(f'Segunda + terceira marchas: {max(time_array_ovt[1]):.2f} s')
    print(f'Terceira marcha: {max(time_array_ovt[2]):.2f} s')
    print(f'Quarta marcha: {max(time_array_ovt[3]):.2f} s')
    print(f'Quinta marcha: {max(time_array_ovt[4]):.2f} s')
    print(f'Sexta marcha: {max(time_array_ovt[5]):.2f} s')
    print(f'Sétima marcha: {max(time_array_ovt[6]):.2f} s')
    print('----- Deslocamento de 60 km/h a 120 km/h -----')
    print(f'Primeira + segunda + terceira marchas: {max(car_displacement_array_ovt[0]):.2f} m')
    print(f'Segunda + terceira marcha: {max(car_displacement_array_ovt[1]):.2f} m')
    print(f'Terceira marcha: {max(car_displacement_array_ovt[2]):.2f} m')
    print(f'Quarta marcha: {max(car_displacement_array_ovt[3]):.2f} m')
    print(f'Quinta marcha: {max(car_displacement_array_ovt[4]):.2f} m')
    print(f'Sexta marcha: {max(car_displacement_array_ovt[5]):.2f} m')
    print(f'Sétima marcha: {max(car_displacement_array_ovt[6]):.2f} m')
    plt.plot(time_array_ovt[0], car_speed_array_ovt[0], label='Primeira + segunda + terceira marcha')
    plt.plot(time_array_ovt[1], car_speed_array_ovt[1], label='Segunda + terceira marcha')
    plt.plot(time_array_ovt[2], car_speed_array_ovt[2], label='Terceira marcha')
    plt.plot(time_array_ovt[3], car_speed_array_ovt[3], label='Quarta marcha')
    plt.plot(time_array_ovt[4], car_speed_array_ovt[4], label='Quinta marcha')
    plt.plot(time_array_ovt[5], car_speed_array_ovt[5], label='Sexta marcha')
    plt.plot(time_array_ovt[6], car_speed_array_ovt[6], label='Sétima marcha')
    plt.xlabel('Tempo [s]')
    plt.ylabel('Velocidade [km/h]')
    yticks = np.arange(0, max(car_speed_array_ovt[6]), 10)
    plt.yticks(yticks, yticks)
    plt.xlim(0,max(time_array_ovt[6]))
    plt.ylim(min(car_speed_array_ovt[6]),max(car_speed_array_ovt[6]))
    plt.legend()
    plt.grid()
    plt.show()

    plt.plot(time_array_ovt[0], car_displacement_array_ovt[0], label='Primeira + segunda + terceira marcha')
    plt.plot(time_array_ovt[1], car_displacement_array_ovt[1], label='Segunda + terceira marcha')
    plt.plot(time_array_ovt[2], car_displacement_array_ovt[2], label='Terceira marcha')
    plt.plot(time_array_ovt[3], car_displacement_array_ovt[3], label='Quarta marcha')
    plt.plot(time_array_ovt[4], car_displacement_array_ovt[4], label='Quinta marcha')
    plt.plot(time_array_ovt[5], car_displacement_array_ovt[5], label='Sexta marcha')
    plt.plot(time_array_ovt[6], car_displacement_array_ovt[6], label='Sétima marcha')
    plt.xlabel('Tempo [s]')
    plt.ylabel('Deslocamento [m]')
    plt.xlim(0,max(time_array_ovt[6]))
    plt.ylim(0,max(car_displacement_array_ovt[6]))
    plt.legend()
    plt.grid()
    plt.show()