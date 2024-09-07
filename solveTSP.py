def nearest_neighbor(num_clients, distances, truck_speed):
    unvisited = list(range(1, num_clients + 1))
    route = [0]  # Start at the depot
    current = 0
    times = {0: 0}  # Dizionario che tiene traccia del tempo di arrivo a ogni nodo, inizia con il deposito a tempo 0
    current_time = 0  # Tempo corrente, inizia da 0

    while unvisited:
        # Trova il nodo più vicino
        nearest = min(unvisited, key=lambda x: distances[current][x])
        
        # Calcola il tempo di arrivo (distanza / velocità del camion)
        travel_time = distances[current][nearest] / truck_speed
        current_time += travel_time
        times[nearest] = current_time
        
        # Aggiorna il percorso e il nodo corrente
        route.append(nearest)
        current = nearest
        unvisited.remove(nearest)

    # Ritorno al deposito
    route.append(0)
    travel_time = distances[current][0] / truck_speed  # Tempo per ritornare al deposito
    current_time += travel_time
    times[0] = current_time  # Aggiorna il tempo di ritorno al deposito

    return route, times

def solveTSP(num_clients, distances, truck_speed, heuristic='nearest_neighbor'):
    if heuristic == 'nearest_neighbor':
        return nearest_neighbor(num_clients, distances, truck_speed)
    else:
        raise ValueError(f"Unsupported heuristic: {heuristic}")
