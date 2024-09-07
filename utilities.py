

def find_subroute_for_j(j,truckSubRoutes):
    """Input: nodo j, truckSubRoutes
        Precondition: j si trova in una subroute ma non si trova nè all'inizio nè alla fine(quindi si trova in una e una sola subroute)
        PostCondition: viene ritornata la lista con la subroute corrispondente
    """
    for subroute_with_flag in truckSubRoutes:
        if j in subroute_with_flag[0]:
            return subroute_with_flag

def updateArrivalTimes(truckRoute, t, maxSavings, start_from):

    pass