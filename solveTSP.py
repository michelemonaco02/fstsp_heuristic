def solveTSP(C, distances_truck, truck_speed):
    # C include i nodi senza il depot, che è 0
    n = len(C)
    
    # Inizializza il percorso partendo e tornando al depot (nodo 0)
    truckRoute = [0]
    
    # Tiene traccia dei nodi visitati
    visited = {0}
    
    # Dizionario che contiene il tempo di arrivo a ogni nodo
    t = {0: 0}  # Il truck parte dal depot al tempo 0

    current_node = 0

    while len(visited) <= n:  # Finché non si visitano tutti i nodi
        nearest_node = None
        nearest_distance = float('inf')

        # Trova il nodo più vicino non ancora visitato
        for node in C:
            if node not in visited and distances_truck[current_node][node] < nearest_distance:
                nearest_node = node
                nearest_distance = distances_truck[current_node][node]

        # Aggiorna il percorso e il tempo
        if nearest_node is not None:
            truckRoute.append(nearest_node)
            visited.add(nearest_node)
            t[nearest_node] = t[current_node] + (nearest_distance / truck_speed)
            current_node = nearest_node

    # Torna al depot (nodo 0)
    truckRoute.append(0)
    t[0] = t[current_node] + (distances_truck[current_node][0] / truck_speed)

    return truckRoute, t
