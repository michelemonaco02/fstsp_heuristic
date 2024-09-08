from solveTSP import solveTSP
import copy

def calcSavings(j,t,truckRoute:list,truckSubRoutes,distances_truck,truck_speed,distances_uav,uav_speed):
    
    index_j = truckRoute.index(j)

    i = truckRoute[index_j - 1]
    k = truckRoute[index_j + 1]

    tau_i_j = distances_truck[i][j] / truck_speed
    tau_j_k = distances_truck[j][k] / truck_speed
    tau_i_k = distances_truck[i][k] / truck_speed
    savings = tau_i_j + tau_j_k - tau_i_k

    #trovo la subroute in cui si trova j
    subroute_with_j = None
    for subroute_with_flag in truckSubRoutes:
        if j in subroute_with_flag[0]:
            subroute_with_j = subroute_with_flag
    
    

    pass

def is_UAV_associated(subroute_with_flag):
    pass

def calcCostTruck():
    pass

def calcCostUAV():
    pass


def performeUpdate():
    pass


def fstsp_heuristic(C,C_prime,distances_truck,truck_speed):
    
    [truckRoute,t] = solveTSP(C,distances_truck,truck_speed)
    truckSubRoutes = [(copy.deepcopy(truckRoute),-1)]
    maxSavings = 0

    while True:
        for j in C_prime:
            calcSavings(j,t,truckRoute)

            for subroute_with_flag in truckSubRoutes:
                if is_UAV_associated(subroute_with_flag):
                    calcCostTruck(j,t,subroute_with_flag)
                else:
                    calcCostUAV(j,t,subroute_with_flag)
        

        if maxSavings > 0:
            performeUpdate()
            maxSavings = 0
        else:
            break


