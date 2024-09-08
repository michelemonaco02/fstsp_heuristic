from solveTSP import solveTSP
import copy
from time import sleep


def print_arrival_times_in_order(t):
    # Ordina il dizionario per tempo di arrivo (i valori del dizionario)
    sorted_arrivals = sorted(t.items(), key=lambda x: x[1])

    # Stampa i nodi in ordine di arrivo con il rispettivo tempo
    print("Tempi di arrivo ordinati:")
    for node, arrival_time in sorted_arrivals:
        print(f"Nodo {node}: {arrival_time:.2f} ore")


def calcSavings(j,t,truckRoute:list,truckSubRoutes,distances_truck,truck_speed,distances_uav,uav_speed,s_r):
    
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
    
    if is_UAV_associated(subroute_with_j):
        a = subroute_with_j[0][0]
        b = subroute_with_j[0][-1]
        j_prime = subroute_with_j[1]

        #Calculate t'[b] , the truck’s arrival time to b if j is removed from the truck route.
        t_prime_b = t[b] - savings

        tau_a_j_prime_uav = distances_uav[a][j_prime] / uav_speed
        tau_j_prime_b_uav = distances_uav[j_prime][b] / uav_speed
        savings = min(savings, t_prime_b - (t[a] + tau_a_j_prime_uav + tau_j_prime_b_uav + s_r))

    return savings

def is_UAV_associated(subroute_with_flag):
    return subroute_with_flag[1] != -1

def calcCostTruck(j,t,subroute_with_flag,distances_truck,truck_speed,savings,e,maxSavings,servedByUAV,best_insertion):
    subroute = subroute_with_flag[0]
    a = subroute[0]
    b = subroute[-1]

    #for all (adjacent i and k in subroute) do
    for index in range(len(subroute) - 1):
        i = subroute[index]
        k = subroute[index + 1]

           # Aggiungi controllo per evitare inserzioni con i == j == k
        if i == j or j == k or i == k:
            continue  # Salta questa iterazione se i, j, o k non sono distinti
        tau_i_j = distances_truck[i][j] / truck_speed
        tau_j_k = distances_truck[j][k] / truck_speed
        tau_i_k = distances_truck[i][k] / truck_speed

        cost = tau_i_j + tau_j_k - tau_i_k
        
        if cost < savings:
            if t[b] - t[a] < e:
                if savings - cost > maxSavings:
                    servedByUAV = False
                    best_insertion = (i,j,k)
                    maxSavings = savings - cost
    

    return servedByUAV,best_insertion,maxSavings

def calcCostUAV(j,t,subroute_with_flag,distances_uav,uav_speed,e,truckRoute,savings,s_l,s_r,maxSavings,servedByUAV,best_insertion):
    
    subroute = subroute_with_flag[0]
    #for all (i and k in subroute, such that i precedes k) do
    for i_index in range(len(subroute) -1):
        i = subroute[i_index]
        for k_index in range(i_index + 1,len(subroute)):
            k = subroute[k_index]

                    # Aggiungi controllo per evitare inserzioni con i == j == k
            if i == j or j == k or i == k:
                continue  # Salta questa iterazione se i, j, o k non sono distinti

            tau_i_j_uav = distances_uav[i][j] / uav_speed
            tau_j_k_uav = distances_uav[j][k] / uav_speed

            if tau_i_j_uav + tau_j_k_uav <= e:
                #Find t’[k], the truck’s arrival time to node k if j were removed from the truck’s route.
                #se j si trova dopo k, t[k] rimane uguale
                if j in truckRoute and truckRoute.index(j) < truckRoute.index(k):
                    t_prime_k = t[k] - savings
                else:
                    t_prime_k = t[k]
                

                cost = max(0 , max((t_prime_k - t[i]) + s_l + s_r, tau_i_j_uav + tau_j_k_uav + s_l + s_r)- (t_prime_k - t[i]))

                if savings - cost > maxSavings:
                    servedByUAV = True
                    best_insertion = (i,j,k)
                    maxSavings = savings - cost

    return servedByUAV,best_insertion,maxSavings



def performeUpdate(best_insertion,servedByUAV,truckRoute,truckSubRoutes,C_prime,t,distances_truck,distances_uav,truck_speed,uav_speed):

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


        for subroute in truckSubRoutes:
            if i in subroute[0] and k in subroute[0]:
                # Salvo l'indice della subroute in truckSubRoutes
                
                index_subroute = truckSubRoutes.index(subroute)


                index_i = subroute[0].index(i)
                index_k = subroute[0].index(k)

                subroute_before_i = subroute[0][:index_i + 1]  # Prima parte fino a i incluso
                subroute_i_k = subroute[0][index_i:index_k + 1]  # Parte tra i e k inclusi
                subroute_after_k = subroute[0][index_k:]  # Parte dopo k

                

                # Rimuovo la subroute originale
                truckSubRoutes.remove(subroute)

                # Inserisco direttamente nella posizione corretta usando index_subroute e lo incremento dopo ogni insert
                if len(subroute_before_i) > 1:
                    truckSubRoutes.insert(index_subroute, (subroute_before_i, -1))
                    index_subroute += 1  # Aggiorno l'indice per la prossima insert

                if len(subroute_i_k) > 1:
                    truckSubRoutes.insert(index_subroute, (subroute_i_k, j))
                    index_subroute += 1  # Aggiorno l'indice per la prossima insert

                if len(subroute_after_k) > 1:
                    truckSubRoutes.insert(index_subroute, (subroute_after_k, -1))
                

                break

        #rimuovo i,j e k da C_prime
        for node in [i, j, k]:
            if node in C_prime:
                C_prime.remove(node)


    else:

        truckRoute.remove(j)

        for subroute in truckSubRoutes:
            #dovrei considerare il caso in cui j si trova agli estremi della subroute?
            #tuttavia, essendo che j appartiene a C_prime, non può appartenere a un estremo di una subroute
            if j in subroute[0]:
                subroute[0].remove(j)
                break
        
        #inserisco j nella sobroute adeguata
        for subroute in truckSubRoutes:
            if i in subroute[0] and k in subroute[0]:
                index_i = subroute[0].index(i)
                index_k = subroute[0].index(k)
                subroute[0].insert(index_i + 1, j)
                break
        
        #inserisco j nella truckRoute
        index_i = truckRoute.index(i)
        truckRoute.insert(index_i + 1, j)

    
    #update dei tempi
    time_update(truckSubRoutes,t,distances_truck,distances_uav,truck_speed,uav_speed)

    print(f"[Performe Update]: Effettuato update con servedByUAV: {servedByUAV}, best_insertion: {best_insertion}.\n"
      f"truckSubRoutes aggiornata: {truckSubRoutes}.\n"
      f"truckRoute aggiornata: {truckRoute}.")

    print_arrival_times_in_order(t)



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
                
                tau_i_j = distances_truck[subroute[index-1]][subroute[index]] / truck_speed
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
                    tau_i_j = distances_truck[subroute[index-1]][subroute[index]] / truck_speed
                    t[subroute[index]] = max(time_uav_arrive,t[subroute[index-1]] + tau_i_j)

                else:
                    tau_i_j = distances_truck[subroute[index-1]][subroute[index]] / truck_speed
                    t[subroute[index]] = t[subroute[index-1]] + tau_i_j


    return



def fstsp_heuristic(C,C_prime,distances_truck,truck_speed,e,distances_uav,uav_speed,s_l,s_r):
    
    [truckRoute,t] = solveTSP(C,distances_truck,truck_speed)
    #il secondo parametro in ogni subRoute è -1 se alla subRoute non è associata la consegna con uav
    #altrimenti nel secondo parametro c'è il nodo che viene servito da uav nella subroute
    truckSubRoutes = [(copy.deepcopy(truckRoute),-1)]
    maxSavings = 0

    while True:
        #ad ogni iterazione, inizializzo servedByUAV e best_insertion
        servedByUAV = False
        best_insertion = None
        
        for j in C_prime:
            savings = calcSavings(j,t,truckRoute,truckSubRoutes,distances_truck,truck_speed,distances_uav,uav_speed,s_r)

            for subroute_with_flag in truckSubRoutes:
                if is_UAV_associated(subroute_with_flag):
                    servedByUAV,best_insertion,maxSavings = calcCostTruck(j,t,subroute_with_flag,distances_truck,truck_speed,savings,e,maxSavings,servedByUAV,best_insertion)
                else:
                    servedByUAV,best_insertion,maxSavings = calcCostUAV(j,t,subroute_with_flag,distances_uav,uav_speed,e,truckRoute,savings,s_l,s_r,maxSavings,servedByUAV,best_insertion)
        

        if maxSavings > 0:
            print(f"[MAIN]: Trovata best insertion {best_insertion} con servedByUAV {servedByUAV} e maxSavings {maxSavings} \n")
            performeUpdate(best_insertion,servedByUAV,truckRoute,truckSubRoutes,C_prime,t,distances_truck,distances_uav,truck_speed,uav_speed)
            maxSavings = 0
        else:
            break

    return truckRoute,t
