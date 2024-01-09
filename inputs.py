# -------------------------------------------- Inputs ---------------------------------------------------

# Ambient
gravity_acceleration = 9.81 # [m/s²]
air_density_sjdc = 1.114 # air density in São José dos Campos [kg/m³]
air_density_0 = 1.225 # mean sea level air density [kg/m³]
kinematic_viscosity_sjdc = 1,778E-05 # kinematic viscosity of air in São José dos Campos [m²/s]
nominal_altitude_sjdc = 646 # nominal altitude in São José dos Campos
nominal_pressure = 93.78644318 # pressure in the nominal altitude [kPa]
gas_constant_air = 0.28697 # gas constant for dry air [kJ/kg.K]
temperature_reference = 25+273 # refence temperature in São José dos Campos [K]
kinematic_viscosity_reference = 1.8e-5


# Ground
ground_shear_coeff = 0.07 # μ


# Motor (Scorpion SII 3026-890 V2 with APC 12X6E)
motor_static_thrust = 34.98 # [N]
motor_decay_coeff = -1.01 # [N/(m/s)]


# Wing
wing_span = 1.82 # [m]
wing_medium_chord = 0.25 # [m]
wing_area = wing_span * wing_medium_chord # [m²]
incidence_wing_cl = 0.7355
incidence_wing_cd = 0.142855
maneuver_wing_cl = 1.5722
maneuver_wing_cd = 0.2164


# Elevator
elevator_area = 0.0966 # [m²]
incidence_elevator_cl = 0.6
incidence_elevator_cd = 0.06
#maneuver_elevator_cl = 0.8
#maneuver_elevator_cd = 0.08
#elevator_efficiency = 0.9
elevator_eta = 0.9 # elevator's efficiency coefficient
horizontal_tail_volume = 0.3


# Rudder
rudder_area = 0.042875 # [m²]
incidence_rudder_cd = 0.0149
rudder_cd = 0.0149
rudder_cd_dp = [rudder_cd]

# Fuselage
fuselage_area = 0.1858 # [m²]
fuselage_cd = 0.1894
fuselage_cd_dp = [fuselage_cd]

# Tailboom
tailboom_area = 0.042412 # [m²]
tailboom_cd = 0.0477
tailboom_cd_dp = [tailboom_cd]


# Individual terms
total_mass = 3.250 # predicted total mass of the airplane [kg]
airplane_stall_angle = 16 # [º]
airplane_incidence_angle = 0 # [º]
airplane_maneuver_angle = 10 # [º]
takeoff_factor = 1.1 # ?
landing_factor = 1.1
approach_factor = 1.2
load_factor_max = 2
alpha_maneuver = 10
takeoff_distance_total = 4.2
takeoff_distance_elevator = 3