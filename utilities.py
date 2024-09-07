

def find_subroute_for_j(j,truckSubRoutes):
    """Input: nodo j, truckSubRoutes
        Precondition: j si trova in una subroute ma non si trova nè all'inizio nè alla fine(quindi si trova in una e una sola subroute)
        PostCondition: viene ritornata la lista con la subroute corrispondente
    """
    for subroute_with_flag in truckSubRoutes:
        if j in subroute_with_flag[0]:
            return subroute_with_flag

def updateArrivalTimesServedByUAV(truckSubRoutes,t,maxSavings,index_subroute_before_i,
                                    index_subroute_i_k,index_subroute_after_k,index_subroute_in,index_subroute_fin,s_l,savings):

    pass

def print_times_in_order(t):
    # Ordina il dizionario t in base ai valori (tempi di arrivo)
    sorted_times = sorted(t.items(), key=lambda item: item[1])
    
    # Stampa i nodi in ordine di arrivo
    for node, time in sorted_times:
        print(f"Node {node}: Time {time}")