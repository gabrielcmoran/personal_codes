from inputs import *
from functions import *
import pandas as pd
import numpy as np

# verificar esses dados
incidence_wing = 0
incidence_elevator = -2
#incidence_elevator = 2
x_cg = -0.08
y_cg = -0.04
x_landing_gear = -0.12
y_landing_gear = -0.2
x_motor = 0.20
y_motor = -0.05
x_wing = -0.0625
y_wing = 0
x_elevator = -0.875
y_elevator = 0.15
x_rudder = -0.875
y_rudder = 0.2
moment_of_inertia_landing_gear = 0.18
stall_angle = 13
elevator_area = 2*elevator_area ######## gambiarra
takeoff_distance = 10
pilot_offset = 3

s1210_dataframe = pd.read_csv('s1210.csv', skiprows=10, index_col=0)
s1210_cl_alpha = s1210_dataframe[['Cl']]
s1210_cd_alpha = s1210_dataframe[['Cd']]
s1210_cm_alpha = s1210_dataframe[['Cm']]

sd7037_dataframe = pd.read_csv('sd7037.csv', skiprows=10, index_col=0)
sd7037_cl_alpha = sd7037_dataframe[['Cl']]
sd7037_cd_alpha = sd7037_dataframe[['Cd']]
sd7037_cm_alpha = sd7037_dataframe[['Cm']]

wing_dataframe = pd.read_csv('wing.csv', skiprows=6, index_col=0)
wing_cl_alpha = wing_dataframe[[' CL']]
wing_cd_alpha = wing_dataframe[[' CD']]
wing_cm_alpha = wing_dataframe[[' Cm']]

elevator_dataframe = pd.read_csv('elevator.csv', skiprows=6, index_col=0)
elevator_cl_alpha = elevator_dataframe[[' CL']]
elevator_cd_alpha = elevator_dataframe[[' CD']]
elevator_cm_alpha = elevator_dataframe[[' Cm']]

elevator_triggered_dataframe = pd.read_csv('elevator_triggered.csv', skiprows=6, index_col=0)
elevator_triggered_cl_alpha = elevator_triggered_dataframe[[' CL']]
elevator_triggered_cd_alpha = elevator_triggered_dataframe[[' CD']]
elevator_triggered_cm_alpha = elevator_triggered_dataframe[[' Cm']]

plot = False

def get_moment(air_density, surface, moment_coeff, velocity):
  return 0.5 * air_density * surface * moment_coeff * velocity ** 2

def takeoff_analysis(motor_static_thrust,motor_decay_coeff,x_motor,y_motor,air_density_sjdc, air_density_0,
                     wing_area,x_wing,y_wing,elevator_area,x_elevator,y_elevator,rudder_area,y_rudder,
                     incidence_rudder_cd,fuselage_area,fuselage_cd,ground_shear_coeff,gravity_acceleration,
                     moment_of_inertia_landing_gear,plot):
    
    # Variables initialization
    total_mass = 2.6 # [kg]
    delta_mass = 0.02 # [kg]
    delta_time = 0.01 # [s]
    displacement_x = 0 # [m]
    maximum_takeoff_alpha = 0.9*stall_angle
    
    while displacement_x < takeoff_distance:
        time = 0 # [s]
        displacement_x = 0 # [m]
        displacement_y = 0 # [m]
        velocity_x = velocity_y = 0 # [m/s]
        angular_velocity = 0 # [rad/s]
        alpha_wing = incidence_wing # [degrees]
        alpha_elevator = incidence_elevator # [degrees]
        alpha_airplane = 0 # [degrees]
        on_ground = True
        going_forward = True
        takeoff_failed = False
        #pilot_triggered = False

        displacement_x_array = []
        displacement_y_array = []
        velocity_x_array = []
        velocity_y_array = []
        angular_velocity_array = []
        alpha_wing_array = []
        total_drag_array = []
        total_lift_array = []
        total_normal_force_array = []
        total_shear_force_array = []
        motor_thrust_array = []
        time_array = []

        while on_ground and going_forward and not takeoff_failed:
            #if displacement_x > (takeoff_distance - pilot_offset) and not pilot_triggered:
            #    alpha_elevator = incidence_elevator + 10
            #    pilot_triggered = True

            motor_thrust = get_motor_thrust(motor_static_thrust, motor_decay_coeff, velocity_x,air_density_sjdc, 
                                            air_density_0)
            motor_thrust_x = motor_thrust*math.cos(math.radians(alpha_airplane))
            motor_thrust_y = motor_thrust*math.sin(math.radians(alpha_airplane))
            motor_thrust_moment = motor_thrust_y*abs(x_landing_gear - x_motor) - motor_thrust_x*abs(y_landing_gear - y_motor)

            cl_wing = np.interp(alpha_wing, wing_cl_alpha.index.values, wing_cl_alpha[' CL'])
            cd_wing = np.interp(alpha_wing, wing_cd_alpha.index.values, wing_cd_alpha[' CD'])
            cm_wing = np.interp(alpha_wing, wing_cm_alpha.index.values, wing_cm_alpha[' Cm'])
            
            cl_elevator = np.interp(alpha_elevator, elevator_cl_alpha.index.values, elevator_cl_alpha[' CL'])
            #cl_elevator = -0.377
            cd_elevator = np.interp(alpha_elevator, elevator_cd_alpha.index.values, elevator_cd_alpha[' CD'])
            cm_elevator = np.interp(alpha_elevator, elevator_cm_alpha.index.values, elevator_cm_alpha[' Cm'])
            
            cl_elevator_triggered = np.interp(alpha_elevator, elevator_triggered_cl_alpha.index.values, elevator_triggered_cl_alpha[' CL'])
            cd_elevator_triggered = np.interp(alpha_elevator, elevator_triggered_cd_alpha.index.values, elevator_triggered_cd_alpha[' CD'])
            cm_elevator_triggered = np.interp(alpha_elevator, elevator_triggered_cm_alpha.index.values, elevator_triggered_cm_alpha[' Cm'])
            
            if displacement_x > (takeoff_distance - pilot_offset):
                cl_elevator = cl_elevator_triggered
                cd_elevator = cd_elevator_triggered
                cm_elevator = cm_elevator_triggered
                #pilot_triggered = True

            #cl_wing = np.interp(alpha_wing, s1210_cl_alpha.index.values, s1210_cl_alpha['Cl'])
            #cd_wing = np.interp(alpha_wing, s1210_cd_alpha.index.values, s1210_cd_alpha['Cd'])
            #cm_wing = np.interp(alpha_wing, s1210_cm_alpha.index.values, s1210_cm_alpha['Cm'])
            #cl_elevator = -1*np.interp(alpha_elevator, sd7037_cl_alpha.index.values, sd7037_cl_alpha['Cl'])
            #cd_elevator = np.interp(alpha_elevator, sd7037_cd_alpha.index.values, sd7037_cd_alpha['Cd'])
            #cm_elevator = -1*np.interp(alpha_elevator, sd7037_cm_alpha.index.values, sd7037_cm_alpha['Cm'])

            wing_lift = get_lift(air_density_sjdc, wing_area, cl_wing, velocity_x)
            wing_drag = get_drag(air_density_sjdc, wing_area, cd_wing, velocity_x)
            wing_moment = get_moment(air_density_sjdc, wing_area, cm_wing, velocity_x)
            wing_lift_moment = wing_lift*abs(x_landing_gear - x_wing)
            wing_drag_moment = wing_drag*abs(y_landing_gear - y_wing)

            elevator_lift = get_lift(air_density_sjdc, elevator_area, cl_elevator, velocity_x)
            elevator_drag = get_drag(air_density_sjdc, elevator_area, cd_elevator, velocity_x)
            elevator_moment = get_moment(air_density_sjdc, elevator_area, cm_elevator, velocity_x)
            elevator_lift_moment = elevator_lift*abs(x_elevator - x_landing_gear)
            elevator_drag_moment = elevator_drag*abs(y_landing_gear - y_elevator)

            rudder_drag = get_drag(air_density_sjdc, rudder_area, incidence_rudder_cd, velocity_x)
            rudder_drag_moment = rudder_drag*abs(y_landing_gear - y_rudder)
            fuselage_drag = get_drag(air_density_sjdc, fuselage_area, fuselage_cd, velocity_x)

            total_weight = get_weight(total_mass, gravity_acceleration)
            weight_moment = total_weight*abs(x_landing_gear - x_cg)

            total_lift = wing_lift + elevator_lift
            total_drag = wing_drag + elevator_drag + rudder_drag + fuselage_drag
            total_moment = (wing_moment + wing_lift_moment + wing_drag_moment + elevator_moment - 
                            elevator_lift_moment + elevator_drag_moment + rudder_drag_moment - weight_moment + 
                            motor_thrust_moment)
            
            total_normal_force = total_weight - total_lift
            total_shear_force = get_shear_force(ground_shear_coeff, total_normal_force)

            sum_forces_x = motor_thrust_x - total_drag - total_shear_force
            sum_forces_y = motor_thrust_y + total_lift + total_normal_force - total_weight

            acceleration_x = get_acceleration(sum_forces_x, total_mass)
            acceleration_y = get_acceleration(sum_forces_y, total_mass)
            angular_acceleration = total_moment/moment_of_inertia_landing_gear

            velocity_x = get_velocity(velocity_x, acceleration_x, delta_time)
            velocity_y = get_velocity(velocity_y, acceleration_y, delta_time)

            displacement_x = get_displacement(displacement_x, velocity_x, delta_time)
            displacement_y = get_displacement(displacement_y, velocity_y, delta_time)

            if angular_acceleration > 0:
                angular_velocity = get_velocity(angular_velocity, angular_acceleration, delta_time)
                delta_alpha_airplane = math.degrees(angular_velocity*delta_time) # fazer funcao talvez
                alpha_airplane = alpha_airplane + delta_alpha_airplane
                if alpha_airplane > maximum_takeoff_alpha:
                    alpha_airplane = maximum_takeoff_alpha
                alpha_wing = alpha_wing + delta_alpha_airplane
                alpha_elevator = alpha_elevator + delta_alpha_airplane

            time = get_time(time, delta_time)
            
            print(f'total: {total_moment:.2f}, wing: {wing_moment:.2f}, wing_lift_m: {wing_lift_moment:.2f}, elevator: {elevator_moment:.2f}, elevator_lift_m: {elevator_lift_moment:.2f}, alpha: {alpha_airplane:.2f}, v: {velocity_x:.2f}, x: {displacement_x:.2f}')

            displacement_y_array.append(displacement_y)
            displacement_x_array.append(displacement_x)
            velocity_x_array.append(velocity_x)
            velocity_y_array.append(velocity_y)
            angular_velocity_array.append(angular_velocity)
            alpha_wing_array.append(alpha_wing)
            total_lift_array.append(total_lift)
            total_drag_array.append(total_drag)
            total_normal_force_array.append(total_normal_force)
            total_shear_force_array.append(total_shear_force)
            motor_thrust_array.append(motor_thrust)
            time_array.append(time_array)
            
            if total_normal_force <= 0:
                on_ground = False
            if displacement_x > takeoff_distance:
                takeoff_failed = True
                total_mass = total_mass - delta_mass
            if displacement_x < -2:
                going_forward = False
        
        total_mass = total_mass + delta_mass
        #break

    if plot == True:
        plt.plot(displacement_x_array,total_lift_array,label = 'Total lift')
        plt.plot(displacement_x_array,total_shear_force_array,label = 'Shear force')
        plt.plot(displacement_x_array,total_drag_array,label = 'Total dragg')
        plt.plot(displacement_x_array,motor_thrust_array,label = 'Motor thrust')
        plt.xlabel('Displacement [m/s]')
        plt.ylabel('Forces [N]')
        plt.title("Forces during takeoff")
        plt.legend()
        plt.xlim(0,takeoff_distance)
        plt.ylim(0,total_lift)
        plt.grid()
        plt.show()

    return total_mass


mtow = takeoff_analysis(motor_static_thrust,motor_decay_coeff,x_motor,y_motor,air_density_sjdc, air_density_0,
                        wing_area,x_wing,y_wing,elevator_area,x_elevator,y_elevator,rudder_area,y_rudder,
                        incidence_rudder_cd,fuselage_area,fuselage_cd,ground_shear_coeff,gravity_acceleration,
                        moment_of_inertia_landing_gear,plot)
print(f'{mtow:.2f} kg')
