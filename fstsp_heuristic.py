from solveTSP import solveTSP
import utilities


def calcSavings(j,t,truckRoute:list,truckSubRoutes,distances_truck,truck_speed,distances_uav,drone_speed,s_r):
    # This function calculates the savings achieved by removing some customer j from the truck’s route.
    
    #trovo l'indice di j
    #sono sicuro che non sia nè alla prima nè alla ultima posizione, poichè il depot non appartiene a C_prime
    index_j = truckRoute.index(j)

    #Find i, the node immediately preceding j in the truck’s route.
    i = truckRoute[index_j - 1]
    k = truckRoute[index_j + 1]

    #savings = tau_i,j + tau_j,k - tau_i,k
    tau_i_j = distances_truck[i][j] / truck_speed
    tau_j_k = distances_truck[j][k] / truck_speed
    tau_i_k = distances_truck[i][k] / truck_speed

    savings = tau_i_j + tau_j_k - tau_i_k

    #trovo la subroute (con flag) in cui si trova j
    subroute_with_flag = utilities.find_subroute_for_j(j,truckSubRoutes)

    if is_UAV_associated(subroute_with_flag):
        #Savings may be limited by the existing UAV assignment
        # (e.g., the truck waits for the UAV to return):

        #Find a, the first node in the truck’s subroute (where the UAV launches).
        a = subroute_with_flag[0][0]
        #Find b, the last node in the truck’s subroute (where the UAV returns).
        b = subroute_with_flag[0][-1]
        #Find j', the customer visited by the UAV associated with this subroute.
        j_prime = subroute_with_flag[1]

        #Calculate t'[b] , the truck’s arrival time to b if j is removed from the truck route.
        t_prime_b = t[b] - savings

        #savings = min{savings, t'[b] - (t[a] + (tau_a,j')' + (tau_j',b)' + s_r)}
        tau_a_j_prime_uav = distances_uav[a][j_prime] / drone_speed
        tau_j_prime_b_uav = distances_uav[j_prime][b] / drone_speed

        savings = min(savings, t_prime_b - (t[a] + tau_a_j_prime_uav + tau_j_prime_b_uav + s_r))

    return savings



def is_UAV_associated(subroute_with_flag):
    return subroute_with_flag[1] != -1

def calcCostTruck(j,t,subroute_with_flag,maxSavings,servedByUAV,distances_truck,truck_speed,savings,e):
    #Find a, the first node in the truck’s subroute.
    #Find b, the last node in the truck’s subroute.
    subroute = subroute_with_flag[0]
    a = subroute_with_flag[0]
    b = subroute_with_flag[-1]

    #for all (adjacent i and k in subroute) do
    for idx in range(len(subroute) - 1) :
        i = subroute[idx]
        k = subroute[idx + 1]

        #mi assicuro che i e k siano diversi da j:
        if i != j and k != j:
            
            #cost = tau_i;j + tau_j,k - tau_i,k
            tau_i_j = distances_truck[i][j] / truck_speed
            tau_j_k = distances_truck[j][k] / truck_speed
            tau_i_k = distances_truck[i][k] / truck_speed

            cost  =tau_i_j + tau_j_k - tau_i_k

            if cost < savings:
                # Can the UAV assigned to this subroute still feasibly fly?
                if (t[b] - t[a] + cost) <= e:
                    if (savings - cost ) > maxSavings:
                        #save this change
                        servedByUAV = False
                        best_insertion = (i,j,k)
                        maxSavings = savings - cost


    return best_insertion

def calcCostUAV(j,t,subroute_with_flag,truckRoute,maxSavings,servedByUAV,distances_uav,drone_speed,e,savings,s_l,s_r):
    # This truck subroute is not associated with a UAV visit
    # Try to use the UAV to visit j
    subroute = subroute_with_flag[0]
    best_insertion = None

    # Ensure savings is a number
    if savings is None:
        savings = 0  # or some other appropriate default value

    #for all (i and k in subroute, such that i precedes k) do
    for i_idx in range(len(subroute) - 1):
        i = subroute[i_idx]
        for k_idx in range(i_idx + 1, len(subroute)):
            k = subroute[k_idx]
            #mi assicuro che j sia diverso da i e k
            if i != j and k != j:
                #if ((tau_i,j)' + (tau_j,k)' <= e) then
                tau_i_j_uav = distances_uav[i][j] / drone_speed
                tau_j_k_uav = distances_uav[j][k] / drone_speed
                if (tau_i_j_uav + tau_j_k_uav) <= e:  # Fixed this condition
                    #Find t'[k], the truck's arrival time to node k if j were removed from the truck's route.
                    #se j si trova dopo k, t[k] rimane uguale
                    if j in truckRoute and truckRoute.index(j) < truckRoute.index(k):
                        t_prime_k = t[k] - savings
                    else:
                        t_prime_k = t[k]
                   
                    #cost = max {0,max{(t'[k]-t[i] + s_l + s_r,(tau_i,j)' + (tau_j,k)' + s_l + s_r} - (t'[k] - t[i])}
                    cost = max(0, max((t_prime_k - t[i]) + s_l + s_r, tau_i_j_uav + tau_j_k_uav + s_l + s_r) - (t_prime_k - t[i]))
                   
                    if savings - cost > maxSavings:  # Changed < to > as we're maximizing savings
                        servedByUAV = True
                        best_insertion = (i,j,k)
                        maxSavings = savings - cost
   
    return best_insertion





def performeUpdate(best_insertion,servedByUAV,C_prime,truckRoute,truckSubRoutes,t,maxSavings):

    i = best_insertion[0]
    j = best_insertion[1]
    k = best_insertion[2]


    if servedByUAV == True:
        #remove j from truckRoute
        truckRoute.remove(j)
        
        # update delle truckSubRoutes
        #elimino j dalla subroute in cui si trovava
        for subroute_with_flag in truckSubRoutes:
            if j in subroute_with_flag[0]:
                subroute_with_flag[0].remove(j)
                break
        

        #supponiamo di aver inserito j in una subroute S con nodi di lancio e retrieve i e k. Spezzo la subroute per aggiornare
        #per prima cosa, trovo la subroute con i e k, poi la elimino e aggiorno
        #NON CREDO SIA GIUSTO. Inoltre, voglio che l'aggiornamento dei truckSubRoutes sia in modo tale che le subroutes siano in ordine
        for subroute in truckSubRoutes:
            if i in subroute[0] and k in subroute[0]:
                index_i = subroute[0].index(i)
                index_k = subroute[0].index(k)

                subroute_before_i = subroute[0][:index_i + 1]
                subroute_i_k = subroute[0][index_i:index_k + 1]
                subroute_after_k = subroute[0][index_k:]

                truckSubRoutes.remove(subroute)

                #tengo conto del caso in cui i e k sono il nodo iniziale o finale
                if len(subroute_before_i) > 1:
                    truckSubRoutes.append((subroute_before_i, -1))
                if len(subroute_i_k) > 1:
                    truckSubRoutes.append((subroute_i_k, j))
                if len(subroute_after_k) > 1:
                    truckSubRoutes.append((subroute_after_k, -1))

                break
        
        #elimino i nodi i j k da C_prime
        for node in [i, j, k]:
            if node in C_prime:
                C_prime.remove(node)





    else:
        for subroute in truckSubRoutes:
            if j in subroute[0]:
                subroute[0].remove(j)
                break
        
        for subroute in truckSubRoutes:
            if i in subroute[0] and k in subroute[0]:
                index_i = subroute[0].index(i)
                index_k = subroute[0].index(k)
                subroute[0].insert(index_i + 1, j)
                break
        
        truckRoute.remove(j)
        index_i = truckRoute.index(i)
        truckRoute.insert(index_i + 1, j)

    
    #come aggiornare t?
    #IDEA: Per i nodi successivi alla subroute modificata, t[node] -= maxSavings, quindi devo gestire solo l'aggiornamento nella subroute modificata.
    #Problema: bisogna tenere conto di eventuali attese del truck per l'UAV

        
            



def fstsp_heuristic(num_clients, C, C_prime, distances_truck, distances_uav, truck_speed, drone_speed, s_l, s_r, e):
    
    truckRoute, t = solveTSP(len(C), distances_truck)
    truckSubRoutes = [(truckRoute,-1)]
    maxSavings = 0

    while True:
        #dichiaro la variabile servedByUAV
        servedByUAV = False
        
        for j in C_prime:

            #trovo il risparmio che ottengo togliendo j dalla truckRoute
            savings = calcSavings(j,t,truckRoute,truckSubRoutes,distances_truck,truck_speed,distances_uav,drone_speed,s_r)
            if savings is None:
                savings = 0  # or some other appropriate default value

            #itero su ogni subroute e valuto se mi conviene aggiugnerci j
            for subroute_with_flag in truckSubRoutes:
                if is_UAV_associated(subroute_with_flag):
                    #passo maxSavings e servedByUAV a calcCostTruck, che eventualmente aggiornerà il valore
                    best_insertion = calcCostTruck(j,t,subroute_with_flag,maxSavings,servedByUAV,distances_truck,truck_speed,savings,e)
                else:
                    best_insertion = calcCostUAV(j,t,subroute_with_flag,truckRoute,maxSavings,servedByUAV,distances_uav,drone_speed,e,savings,s_l,s_r)

        #se ho trovato miglioramenti, faccio l'update
        if maxSavings > 0:
            print(f"[MAIN]: Ho trovato un miglioramento {best_insertion} con servedByUav {servedByUAV}...")
            performeUpdate(best_insertion,servedByUAV,C_prime,truckRoute,truckSubRoutes,t,maxSavings)
            maxSavings = 0

        #non ci sono miglioramenti, interrompo l'algoritmo
        else:
            break

    


