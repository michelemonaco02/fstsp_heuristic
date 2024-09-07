import pandas as pd
from fstsp_heuristic import fstsp_heuristic
from solveTSP import solveTSP

def load_distances_small(truck=True):
    if truck:
        return pd.DataFrame({
            0: [0, 10, 15, 20, 25, 30],
            1: [10, 0, 12, 18, 22, 28],
            2: [15, 12, 0, 10, 16, 24],
            3: [20, 18, 10, 0, 8, 18],
            4: [25, 22, 16, 8, 0, 10],
            5: [30, 28, 24, 18, 10, 0]
        })
    else:
        return pd.DataFrame({
            0: [0, 6, 9, 12, 14, 16],
            1: [6, 0, 5, 8, 10, 13],
            2: [9, 5, 0, 4, 6, 9],
            3: [12, 8, 4, 0, 3, 6],
            4: [14, 10, 6, 3, 0, 5],
            5: [16, 13, 9, 6, 5, 0]
        })

def load_parameters_small():
    return {
        'service time for van': 300,  # seconds
        'flight time_large baterry': 1800,  # seconds (30 minutes endurance)
        'drone capacity': 5,  # kg
        'launch time_100 m': 60,  # seconds
        'landing time_100m': 60,  # seconds
        'preparation time before each launch': 180,  # seconds
        'service time for drones': 180  # seconds
    }

def analyze_drone_speed_impact_on_fstsp():
    # Numero di clienti ridotto per test
    num_clients = 5

    # Carica i parametri del drone e del van
    drone_params = load_parameters_small()

    # Estrai e converte i parametri
    truck_speed = 40  # km/h fixed for the truck
    service_time_van = float(drone_params['service time for van'])  # seconds for each customer

    drone_endurance = float(drone_params['flight time_large baterry']) / 3600  # Convert to hours
    drone_capacity = float(drone_params['drone capacity'])  # kg
    launch_time = float(drone_params['launch time_100 m']) / 3600  # Convert to hours
    landing_time = float(drone_params['landing time_100m']) / 3600  # Convert to hours
    preparation_time = float(drone_params['preparation time before each launch'])  # seconds
    service_time_drone = float(drone_params['service time for drones'])  # seconds for each customer

    # Carica le distanze
    distances_truck = load_distances_small(truck=True)
    distances_uav = load_distances_small(truck=False)

    
    drone_speeds = [32]  # km/h

    for drone_speed in drone_speeds:
        # Esegui l'algoritmo FSTSP con la velocità del drone variabile
        print(f"\nTesting with {num_clients} clients and drone speed: {drone_speed} km/h")

        # Parametri per la funzione fstsp_heuristic
        s_l = launch_time
        s_r = landing_time
        e = drone_endurance  # Endurance

        C = list(range(1, num_clients + 1))  # C = {1, 2, ..., n}
        C_prime = C  # For now, assume all customers are UAV-eligible

        fstsp_heuristic(
            num_clients,
            C,
            C_prime,
            distances_truck,
            distances_uav,
            truck_speed,
            drone_speed,
            s_l,
            s_r,
            e
        )

        print(f"Finished testing with drone speed: {drone_speed} km/h\n")

if __name__ == "__main__":
    analyze_drone_speed_impact_on_fstsp()
