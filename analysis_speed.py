import os
import pandas as pd
import numpy as np
from data_loader import load_distances, load_parameters
from fstsp_heuristic import fstsp_heuristic
from solveTSP import solveTSP

# Funzione per convertire i parametri in float
def convert_to_float(value):
    if isinstance(value, str):
        return float(value.replace('kg', '').replace('sec', '').replace(' ', '').replace('[','').replace(']',''))
    return float(value)

# Funzione per gestire la conversione dei pesi dei clienti
def parse_demand(demand_str):
    return [convert_to_float(x) for x in demand_str.strip('[] kg').split(',')]

def analyze_drone_speed_impact_on_fstsp():
    # Lista di file da analizzare (solo scenari urbani)
    files = [
        "Van_Urban_40.xlsx",
        #"Van_Urban_60.xlsx",
        #"Van_Urban_100.xlsx",
        "Drone_Urban_40.xlsx",
        #"Drone_Urban_60.xlsx",
        #"Drone_Urban_100.xlsx"
    ]

    base_path = 'Data_and_data-description/TELIKA DATA/'
    
    #num_clients_list = [40, 60, 100]  # Numero di clienti per l'analisi
    num_clients_list = [40]
    # Range di velocità del drone da testare (in km/h)
    drone_speeds = [32, 40, 48, 56, 64] 

    # Lista per salvare i risultati
    results = []

    # Testa tutte le combinazioni di file, numero di clienti e velocità del drone
    for num_clients in num_clients_list:
        demand_category = f'{num_clients} clients'

        # Carica i parametri del drone e del van
        drone_params = load_parameters(os.path.join(base_path, 'Values of parameters for drone routing.xlsx'), demand_category)

        # Estrai e converte i parametri
        customer_weights = parse_demand(drone_params[f'demand_{demand_category}'])
        truck_speed = 40  # km/h fisso per il truck
        service_time_van = convert_to_float(drone_params['service time for van'])  # secondi per ogni cliente

        drone_endurance = convert_to_float(drone_params['flight time_large baterry']) / 3600  # Converti in ore
        drone_capacity = convert_to_float(drone_params['drone capacity'])  # kg
        launch_time = convert_to_float(drone_params['launch time_100 m'])  # secondi
        landing_time = convert_to_float(drone_params['landing time_100m'])  # secondi
        preparation_time = convert_to_float(drone_params['preparation time before each launch'])  # secondi
        service_time_drone = convert_to_float(drone_params['service time for drones'])  # secondi per ogni cliente

        # Trova i file corrispondenti al numero di clienti
        truck_file = f"Van_Urban_{num_clients}.xlsx"
        uav_file = f"Drone_Urban_{num_clients}.xlsx"

        if truck_file in files and uav_file in files:
            # Carica le distanze
            distances_truck = load_distances(os.path.join(base_path, truck_file))
            distances_uav = load_distances(os.path.join(base_path, uav_file))

            
            for drone_speed in drone_speeds:
                # Esegui l'algoritmo FSTSP con la velocità del drone variabile
                fstsp_heuristic(
                    distances_truck, distances_uav, customer_weights,
                    truck_speed=truck_speed, drone_speed=drone_speed, drone_endurance=drone_endurance, 
                    drone_capacity=drone_capacity, launch_time=launch_time, landing_time=landing_time, 
                    preparation_time=preparation_time, service_time_van=service_time_van, service_time_drone=service_time_drone
                )

                

  
if __name__ == "__main__":
    analyze_drone_speed_impact_on_fstsp()
