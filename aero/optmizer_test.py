import pyswarms as ps
import numpy as np
from pyswarms.utils.functions import single_obj as fx
from pyswarms.utils.plotters import plot_contour, plot_surface, plot_cost_history
from pyswarms.utils.plotters.formatters import Designer, Mesher
from parameters.parameters import plane_parameters
from components.plane import Plane
from performance.takeoff_class import Takeoff
from flight_score import Flight_score
from functools import partial



# Bounds
min_profile = 0
max_profile = 1.5

min_wing_chord_1th_section = 0.15 # fazer funcao de condição
max_wing_chord_1th_section = 0.5
min_wing_chord_2th_section = 0.15
max_wing_chord_2th_section = 0.5
min_wing_chord_3th_section = 0.15
max_wing_chord_3th_section = 0.5
min_wing_span_1th_to_2th_section = 0.1 # fazer funcao de condição
max_wing_span_1th_to_2th_section = 1.5
min_wing_span_2th_to_3th_section = 0
max_wing_span_2th_to_3th_section = 1.5
min_wing_incidence = 0
max_wing_incidece = 5

min_horizontal_stabilizer_chord_1th_section = 0.1 # fazer funcao de condição
max_horizontal_stabilizer_chord_1th_section = 0.4
min_horizontal_stabilizer_chord_2th_section = 0.1
max_horizontal_stabilizer_chord_2th_section = 0.4
min_horizontal_stabilizer_chord_3th_section = 0.1
max_horizontal_stabilizer_chord_3th_section = 0.4
min_horizontal_stabilizer_span_1th_to_2th_section = 0.05 # fazer funcao de condição
max_horizontal_stabilizer_span_1th_to_2th_section = 0.5
min_horizontal_stabilizer_span_2th_to_3th_section = 0
max_horizontal_stabilizer_span_2th_to_3th_section = 0.5
min_horizontal_stabilizer_incidence = -5 # fazer condicao de perfil invertido ou nao
max_horizontal_stabilizer_incidece = 5


parameters = {
    "a": 1,
    "b": 2,
    "c": 3
}
def get_plane_p():
    return plane_parameters

def score(values,coisa):
    score_array = []
    for item in values:
        new_parameters = plane_parameters
        new_parameters["wing_span_1th_to_2th_section"] = item[0]
        new_parameters["wing_span_2th_to_3th_section"] = item[1]
        new_parameters["wing_chord_1th_section"] = item[2]
        plane = Plane(new_parameters)
        score = coisa*plane.wing.area
        score_array.append(score)
    #return np.array(score_array).squeeze()
    return score_array

flight_score = Flight_score()
bounds= ([1,1,2], [3,4,5])
#bounds= np.array([[1,], [3]])

#plane = Plane(plane_parameters)
#gravity = 9.81

# Set-up hyperparameters
options = {'c1': 0.5, 'c2': 0.3, 'w':0.9}
# Call instance of PSO
optimizer = ps.single.GlobalBestPSO(n_particles=20, dimensions=3, options=options, bounds=bounds)
# Perform optimization
#new_score = partial(score,coisa=2)
best_cost, best_pos = optimizer.optimize(flight_score.score, iters=100)
#cost_plot = plot_cost_history(cost_history = optimizer.cost_history)
#cost_plot.figure.savefig('file_name.jpg')