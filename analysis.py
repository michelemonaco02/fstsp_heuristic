import os
import pandas as pd
from data_loader import load_distances, load_parameters
from fstsp_heuristic import fstsp_heuristic
from solveTSP import solveTSP
from map_visualizer import visualize_fstsp

def analyze_drone_speed_impact_on_fstsp():
    base_path = 'Data_and_data-description/TELIKA DATA/'
    
    num_clients = 8  # Fixed number of clients

    # Range di velocità del drone da testare (in km/h)
    drone_speeds = [32]  # Potrai aggiungere ulteriori valori di velocità per espandere il test

    # Carica i parametri del drone e del van
    drone_params = load_parameters(os.path.join(base_path, 'Values of parameters for drone routing.xlsx'), '40 clients')

    # Estrai e converte i parametri
    customer_weights = drone_params['demand_40 clients'][:num_clients]  # Take only the first 8 weights
    truck_speed = 40  # km/h fixed for the truck
    service_time_van = float(drone_params['service time for van'])  # seconds for each customer

    drone_endurance = float(drone_params['flight time_large baterry']) / 3600  # Convert to hours
    drone_capacity = float(drone_params['drone capacity'])  # kg
    launch_time = float(drone_params['launch time_100 m']) / 3600 # convert to hours
    landing_time = float(drone_params['landing time_100m']) / 3600 # convert to hours
    preparation_time = float(drone_params['preparation time before each launch'])  # seconds
    service_time_drone = float(drone_params['service time for drones'])  # seconds for each customer

    # Carica le distanze
    distances_truck = load_distances(os.path.join(base_path, 'Van_Urban_40.xlsx'))[:num_clients+1, :num_clients+1]
    distances_uav = load_distances(os.path.join(base_path, 'Drone_Urban_40.xlsx'))[:num_clients+1, :num_clients+1]

    # Risolvi il problema TSP con una euristica standard (es: nearest neighbor)
    truck_route, truck_times = solveTSP(num_clients, distances_truck, heuristic='nearest_neighbor')
    
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

        # Generate client coordinates (for visualization purposes)
        clients = [(x, y) for x in range(3) for y in range(3) if x * 3 + y < num_clients]
        depot = (1, 1)  # Place depot in the center

        # Visualize the solution
        visualize_fstsp(clients, depot, truck_route)

        print(f"Finished testing with drone speed: {drone_speed} km/h\n")

if __name__ == "__main__":
    analyze_drone_speed_impact_on_fstsp()
