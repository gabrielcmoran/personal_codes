import math
import numpy as np

#mission_type = 'complete'
#empty_weight_error = 0.1
#mission_time = 420
#empty_weight = 1.5
payload = 2

def get_flight_score(values):
    mission_type = 'complete'
    empty_weight_error = 0.1
    mission_time = 420
    empty_weight = 1.5
    pontuation = []
    
    for item in values:
        payload = item[0]
        empty_weight = item[1]
        # FTP
        if mission_type == 'initial':
            FTP = 1
        if mission_type == 'complete':
            FTP = 1.35

        # FPV
        FPV = max((1.05 - 10*(empty_weight_error**2.2)), 0.95)

        # FTM
        FTM = max((1/(1+math.exp((mission_time - 261)/33.88 - 6.1))), 0.1)

        # structural_efficiency
        structural_efficiency = payload/empty_weight

        # flight score
        flight_score = FTP*FPV*FTM*135*(payload**0.2)*(0.4 + 0.66/(1+math.exp((1.75-structural_efficiency)/0.8 + 0.3)))
        pontuation.append(flight_score)
    return np.array(pontuation).squeeze()


#flight_score = get_flight_score(mission_type,empty_weight_error,mission_time,payload,empty_weight)[1]
#structural_efficiency = get_flight_score(mission_type,empty_weight_error,mission_time,payload,empty_weight)[0]
#print(f"Flight score: {flight_score:.2f}")