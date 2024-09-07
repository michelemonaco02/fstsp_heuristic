def nearest_neighbor(num_clients, distances):
    unvisited = list(range(1, num_clients + 1))
    route = [0]  # Start at the depot
    current = 0
    times = {0: 0}  # Dizionario che tiene traccia del tempo di arrivo a ogni nodo, inizia con il deposito a tempo 0
    current_time = 0  # Tempo corrente, inizia da 0

    while unvisited:
        # Trova il nodo più vicino
        nearest = min(unvisited, key=lambda x: distances[current][x])
        
        # Aggiorna il tempo di arrivo per il nodo più vicino
        current_time += distances[current][nearest]
        times[nearest] = current_time
        
        # Aggiorna il percorso e il nodo corrente
        route.append(nearest)
        current = nearest
        unvisited.remove(nearest)

    # Ritorno al deposito
    route.append(0)
    current_time += distances[current][0]
    times[0] = current_time  # Aggiorna il tempo di ritorno al deposito

    return route, times

def solveTSP(num_clients, distances, heuristic='nearest_neighbor'):
    if heuristic == 'nearest_neighbor':
        return nearest_neighbor(num_clients, distances)
    else:
        raise ValueError(f"Unsupported heuristic: {heuristic}")
