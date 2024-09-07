

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

    #salvo la lunghezza di truckSubRoutes
    len_truckSubRoutes = len(truckSubRoutes)
    #caso 1.1 S_in = S_fin
    if index_subroute_in == index_subroute_fin:
        #per i clienti dopo k, t[cliente] -= maxSavings
        for index in range(index_subroute_after_k,len_truckSubRoutes):
            for client in truckSubRoutes[index][0]:
                t[client] -= maxSavings
    
    #per i clienti in quella subroute ???

    #caso 1.2: S_fin < S_in
    elif index_subroute_fin < index_subroute_in:  
        #Per i clienti compresi tra i e k: t[cliente] += s_l (tempo richiesto per il lancio)
        for client in truckSubRoutes[index_subroute_i_k][0]:
            t[client] += s_l

        #per i clienti dopo k, t[cliente] += maxSavings
        for index in range(index_subroute_after_k,len_truckSubRoutes):
            for client in truckSubRoutes[index][0]:
                t[client] -= maxSavings

    #caso 1.3: S_fin > S_in
    else:
        #Dal cliente successive a j, fino a i: t[cliente] -= savings (savings = tau_i,j + tau_j,k - tau_i,k)
        for index in range(index_subroute_in,index_subroute_before_i):
            for client in truckSubRoutes[index][0]:
                t[client] -= savings

        #Dal cliente i al cliente k: t[cliente] = t[cliente] – savings + s_l
        for client in truckSubRoutes[index_subroute_i_k][0]:
            t[client] = t[client] - savings + s_l

        #Dal cliente k in poi: t[cliente] -= maxSavings
        #per i clienti dopo k, t[cliente] += maxSavings
        for index in range(index_subroute_after_k,len_truckSubRoutes):
            for client in truckSubRoutes[index][0]:
                t[client] -= maxSavings

def print_times_in_order(t):
    # Ordina il dizionario t in base ai valori (tempi di arrivo)
    sorted_times = sorted(t.items(), key=lambda item: item[1])
    
    # Stampa i nodi in ordine di arrivo
    for node, time in sorted_times:
        print(f"Node {node}: Time {time}")