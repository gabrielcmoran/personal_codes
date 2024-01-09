# ---------------------------------------- Base functions -----------------------------------------------

from inputs import *
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import math
from time import sleep


def get_lift(air_density, surface, lift_coeff, velocity):
  return 0.5 * air_density * surface * lift_coeff * velocity ** 2

def get_drag(air_density, surface, drag_coeff, velocity):
  return 0.5 * air_density * surface * drag_coeff * velocity ** 2

def get_shear_force(shear_coeff, normal_force):
  return shear_coeff * normal_force

def get_motor_thrust(static_thrust, decay_coeff, velocity, air_density_local, air_density_base):
  return max(0, (static_thrust + decay_coeff * velocity)*(air_density_local / air_density_base))

def get_weight(total_mass, gravity_acceleration):
    return total_mass * gravity_acceleration

def get_normal_force(weight,lift):
    return weight - lift

def get_sum_forces_x(thrust, drag, shear):
    return thrust - drag - shear

def get_sum_forces_y(lift, normals, weight):
    return lift + normals - weight

def get_acceleration(force, mass):
    return force / mass

def get_velocity(velocity, acceleration, delta_time):
    return velocity + acceleration*delta_time

def get_displacement(displacement, velocity, delta_time):
    return displacement + velocity*delta_time

def get_time(time, delta_time):
    return time + delta_time

def get_coeff(arrayone, arraytwo, degree): # function to get coeffs from any equation
    polyfit = np.polyfit(arrayone, arraytwo, degree)
    return polyfit

def get_cl(weight, wing_surface, air_density, velocity):
    return (2*weight)/(wing_surface*air_density*(velocity ** 2))

def get_array_csv(column, csvfile):
    dataframe = pd.DataFrame(pd.read_csv(f'{csvfile}.csv', delimiter=';')) # add oficial CSV file
    return np.array(dataframe[column])

def get_cl(weight, wing_surface, air_density, velocity):  #returns the lift coeff needed
    return (2* weight)/(wing_surface*air_density*(velocity ** 2))

def get_cd(thrust, wing_surface, air_density, velocity): #returns the max bearable drag coeff 
    return (2* thrust)/(wing_surface*air_density*(velocity ** 2))

def get_available_thrust(static_thrust, velocity, coeff_decay, air_density, air_density_0):
    available_thrust = ((static_thrust + (velocity * coeff_decay)))*(air_density/air_density_0)
    return available_thrust

def get_required_thrust(weight,cl,cd):
    return weight/(cl/cd)

def get_available_power(available_thrust, velocity):
    return available_thrust * velocity

def get_required_power(required_thrust, velocity):
    return required_thrust * velocity

def get_rate_of_climb(required_power,available_power,weight):
    return (available_power - required_power) / weight

def get_coeff_in_refference(wing_area, component_area, coeff_component):
    coeff_component =  [i * (component_area / wing_area) for i in coeff_component]
    return coeff_component

def get_plot(x_array, y_array, xlabel, ylabel, suptitle):
    plt.plot(x_array, y_array)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.suptitle(suptitle)
    plt.grid(True)

def get_elevator_delta(alpha, wing_cm_alpha_coeff1, wing_cm_alpha_coeff0, horizontal_tail_volume, 
elevator_cl_alpha_coeff1, elevator_cl_alpha_coeff0):
    return ((wing_cm_alpha_coeff1*alpha + wing_cm_alpha_coeff0)/horizontal_tail_volume - 
    elevator_cl_alpha_coeff0)/elevator_cl_alpha_coeff1