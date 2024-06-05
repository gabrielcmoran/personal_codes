import math
import matplotlib.pyplot as plt
import pandas as pd

#           car data
# tires
widht_front_tire = 245 # [mm]
widht_rear_tire = 265 # [mm]
height_to_widht_ratio = 40*0.01 # [-]
rim_diameter = 18 # [pol]
slip = 0.02 # [-]
front_tire_external_diameter = 2*height_to_widht_ratio*widht_front_tire + rim_diameter*25.4 # [mm]
rear_tire_external_diameter = 2*height_to_widht_ratio*widht_rear_tire + rim_diameter*25.4 # [mm]
front_tire_static_radius = 0.47*front_tire_external_diameter # [mm]
rear_tire_static_radius = 0.47*rear_tire_external_diameter # [mm]
front_tire_dinamic_radius = 1.02*front_tire_static_radius # [mm]
rear_tire_dinamic_radius = 1.02*rear_tire_static_radius # [mm]

# transmission
gear_ratio_1st_gear = 4.78 # [:1]
gear_ratio_2st_gear = 2.933 # [:1]
gear_ratio_3st_gear = 2.153 # [:1]
gear_ratio_4st_gear = 1.678 # [:1]
gear_ratio_5st_gear = 1.39 # [:1]
gear_ratio_6st_gear = 1.203 # [:1]
gear_ratio_7st_gear = 1 # [:1]
final_drive_ratio = 3.154 # [:1]

# engine
engine_rotation_cut = 8400 # [rpm]
engine_minimum_rotation = 1000 # [rpm]



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
        tangencial_speed_tire = wheel_rotation_speed*((front_tire_dinamic_radius+rear_tire_dinamic_radius)/2)*10**-3
        car_speed = 3.6*tangencial_speed_tire*(1 - slip)
        engine_rotaton_in_gear_array.append(engine_rotation)
        speed_in_gear_array.append(car_speed)
        engine_rotation = engine_rotation + 50
    speed_array.append(speed_in_gear_array)
    engine_rotation_array.append(engine_rotaton_in_gear_array)

#print(engine_rotation_array[1])
#print(speed_array[1])

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


dataframe1 = pd.read_csv('torque.csv')
omega1 = dataframe1['omega'].tolist()
torque = dataframe1['torque'].tolist()

dataframe2 = pd.read_csv('potencia.csv')
omega2 = dataframe2['omega'].tolist()
power = dataframe2['power'].tolist()

plt.plot(omega1,torque)
plt.plot(omega2,power)
plt.show()