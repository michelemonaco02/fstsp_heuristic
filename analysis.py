import os
import pandas as pd
from data_loader import load_distances, load_parameters
from fstsp_heuristic import fstsp_heuristic
from solveTSP import solveTSP

def analyze_drone_speed_impact_on_fstsp():
    # Lista di file da analizzare (solo scenari urbani)
    files = [
        "Van_Urban_40.xlsx",
        "Van_Urban_60.xlsx",
        "Van_Urban_100.xlsx",
        "Drone_Urban_40.xlsx",
        "Drone_Urban_60.xlsx",
        "Drone_Urban_100.xlsx"
    ]

    base_path = 'Data_and_data-description/TELIKA DATA/'
    
    num_clients_list = [40, 60, 100]  # Numero di clienti per l'analisi

    # Range di velocità del drone da testare (in km/h)
    drone_speeds = [32]  # Potrai aggiungere ulteriori valori di velocità per espandere il test

    # Testa tutte le combinazioni di file, numero di clienti e velocità del drone
    for num_clients in num_clients_list:
        demand_category = f'{num_clients} clients'

        # Carica i parametri del drone e del van
        drone_params = load_parameters(os.path.join(base_path, 'Values of parameters for drone routing.xlsx'), demand_category)

        # Estrai e converte i parametri
        customer_weights = [float(weight) for weight in drone_params[f'demand_{demand_category}']]
        truck_speed = 40  # km/h fisso per il truck
        service_time_van = float(drone_params['service time for van'])  # secondi per ogni cliente

        drone_endurance = float(drone_params['flight time_large baterry']) / 3600  # Converti in ore
        drone_capacity = float(drone_params['drone capacity'])  # kg
        launch_time = float(drone_params['launch time_100 m'])  # secondi
        landing_time = float(drone_params['landing time_100m'])  # secondi
        preparation_time = float(drone_params['preparation time before each launch'])  # secondi
        service_time_drone = float(drone_params['service time for drones'])  # secondi per ogni cliente

        # Trova i file corrispondenti al numero di clienti
        truck_file = f"Van_Urban_{num_clients}.xlsx"
        uav_file = f"Drone_Urban_{num_clients}.xlsx"

        if truck_file in files and uav_file in files:
            # Carica le distanze
            distances_truck = load_distances(os.path.join(base_path, truck_file))
            distances_uav = load_distances(os.path.join(base_path, uav_file))

            # Risolvi il problema TSP con una euristica standard (es: nearest neighbor)
            truck_route, truck_times = solveTSP(num_clients, distances_truck, heuristic='nearest_neighbor')
            
            for drone_speed in drone_speeds:
                # Esegui l'algoritmo FSTSP con la velocità del drone variabile
                print(f"\nTesting with {num_clients} clients and drone speed: {drone_speed} km/h")
                
                # Parametri per la funzione fstsp_heuristic
                s_l = launch_time
                s_r = landing_time
                e = drone_endurance  # Endurance

                # Poiché al momento la funzione non ritorna nulla, monitoriamo il log per osservare i cambiamenti
                C = list(range(1, num_clients + 1))  # C = {1, 2, ..., n}
                C_prime = C  # Al momento C_prime è uguale a C

                fstsp_heuristic(
                    C, C_prime, distances_truck, distances_uav, 
                    truck_speed, drone_speed, s_l, s_r, e
                )

                print(f"Finished testing with drone speed: {drone_speed} km/h\n")

if __name__ == "__main__":
    analyze_drone_speed_impact_on_fstsp()
