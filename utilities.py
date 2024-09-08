

def find_subroute_for_j(j,truckSubRoutes):
    """Input: nodo j, truckSubRoutes
        Precondition: j si trova in una subroute ma non si trova nè all'inizio nè alla fine(quindi si trova in una e una sola subroute)
        PostCondition: viene ritornata la lista con la subroute corrispondente
    """
    for subroute_with_flag in truckSubRoutes:
        if j in subroute_with_flag[0]:
            return subroute_with_flag

def time_update(truckSubRoutes,t:dict,distances_truck, distances_uav, truck_speed, drone_speed):
    
    #initialize t = 0 for every node
    for key in t.keys():
        t[key] = 0

    for subroute_with_flag in truckSubRoutes:
        subroute = subroute_with_flag[0]

        a = subroute[0]
        b = subroute[-1]


        for index in range(1,len(subroute)):
            #se non sono nell'ultima posizione
            if index != len(subroute) - 1:
                
                tau_i_j = distances_truck[subroute[index-1]][index] / truck_speed
                t[subroute[index]] = t[subroute[index-1]] + tau_i_j
            
            else:
                #sono nell'ultima posizione, devo coordinare col drone (se c'è)
                if subroute_with_flag[1] != -1:
                    #trovo j'
                    j_prime = subroute_with_flag[1]
                    #trovo tau_a_j_prime_uav, tau_j_prime_b_uav
                    tau_a_j_prime_uav = distances_uav[a][j_prime] / drone_speed
                    tau_j_prime_b_uav = distances_uav[j_prime][b] / drone_speed

                    #trovo il tempo di arrivo dell'uav a b
                    time_uav_arrive = t[a] + tau_a_j_prime_uav + tau_j_prime_b_uav

                    #eventualmente,in b il truck aspetta per il drone
                    tau_i_j = distances_truck[subroute[index-1]][index] / truck_speed
                    t[subroute[index]] = max(time_uav_arrive,t[subroute[index-1]] + tau_i_j)

                else:
                    tau_i_j = distances_truck[subroute[index-1]][index] / truck_speed
                    t[subroute[index]] = t[subroute[index-1]] + tau_i_j


    return

def stampa_dizionario_ordinato(tempi_arrivo):
    # Filtra i valori diversi da 0
    tempi_arrivo_filtrato = {nodo: tempo for nodo, tempo in tempi_arrivo.items() if tempo != 0}

    # Ordina il dizionario per i tempi di arrivo (valori)
    tempi_arrivo_ordinato = dict(sorted(tempi_arrivo_filtrato.items(), key=lambda item: item[1]))

    # Stampa il dizionario ordinato
    for nodo, tempo in tempi_arrivo_ordinato.items():
        print(f'{nodo}: {tempo}')