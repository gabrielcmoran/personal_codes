import pyswarms as ps
import numpy as np
from pyswarms.utils.functions import single_obj as fx
from flight_score import get_flight_score
# Set-up hyperparameters
options = {'c1': 0.5, 'c2': 0.3, 'w':0.9}
# Call instance of PSO
bounds= np.array([[1,1],[2,1]])
optimizer = ps.single.GlobalBestPSO(n_particles=100, dimensions=2, options=options, bounds=bounds)
# Perform optimization
best_cost, best_pos = optimizer.optimize(get_flight_score, iters=100)