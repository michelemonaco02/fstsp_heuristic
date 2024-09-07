import numpy as np

def nearest_neighbor(num_clients, distances):
    unvisited = list(range(1, num_clients + 1))
    route = [0]  # Start at the depot
    current = 0
    times = [0]  # Time at each node, starting with 0 at the depot

    while unvisited:
        nearest = min(unvisited, key=lambda x: distances[current][x])
        route.append(nearest)
        times.append(times[-1] + distances[current][nearest])
        current = nearest
        unvisited.remove(nearest)

    # Return to depot
    route.append(0)
    times.append(times[-1] + distances[current][0])

    return route, times

def solveTSP(num_clients, distances, heuristic='nearest_neighbor'):
    if heuristic == 'nearest_neighbor':
        return nearest_neighbor(num_clients, distances)
    else:
        raise ValueError(f"Unsupported heuristic: {heuristic}")