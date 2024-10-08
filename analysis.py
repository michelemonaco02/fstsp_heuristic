import os
import pandas as pd
from data_loader import load_distances, load_parameters
from fstsp_heuristic import fstsp_heuristic
from solveTSP import solveTSP

# Funzione per convertire i parametri in float, rimuovendo unità come 'sec' e 'kg'
def convert_to_float(value):
    if isinstance(value, str):
        return float(value.replace('kg', '').replace('sec', '').replace(' ', '').replace('[', '').replace(']', ''))
    return float(value)

# Funzione per gestire la conversione dei pesi dei clienti
def parse_demand(demand_str):
    return [convert_to_float(x) for x in demand_str.strip('[] kg').split(',')]

def analyze_vdrpmdpc_simulation():
    # Lista di file da analizzare, escludendo quelli con 100 clienti e scenari semi-urbani per 40 e 60 clienti
    files = [
        "Van_Urban_60.xlsx",
        "Van_Urban_40.xlsx",
        "Van_Semi-Urban_20.xlsx",
        "Drone_Urban_60.xlsx",
        "Drone_Urban_40.xlsx",
        "Drone_Semi-Urban_20.xlsx"
    ]

    base_path = 'Data_and_data-description/TELIKA DATA/'
    
    num_clients_list = [20, 40, 60]  # Numero di clienti per l'analisi

    # Range di velocità del drone da testare (da 20 a 56 km/h ad intervalli di 9 km/h)
    drone_speeds = range(20, 57, 9)

    # Velocità costante del truck
    truck_speed = 40  # km/h fisso per il truck

    # Per memorizzare i risultati finali
    results = []

    # Testa tutte le combinazioni di file, numero di clienti e velocità del drone
    for num_clients in num_clients_list:
        demand_category = f'{num_clients} clients'

        # Carica i parametri del drone e del van
        drone_params = load_parameters(os.path.join(base_path, 'Values of parameters for drone routing.xlsx'), demand_category)

        drone_endurance = convert_to_float(drone_params['flight time_large baterry']) / 3600  # Converti in ore

        # Trova i file corrispondenti al numero di clienti
        if num_clients == 20:
            van_file = f"Van_Semi-Urban_{num_clients}.xlsx"
            uav_file = f"Drone_Semi-Urban_{num_clients}.xlsx"
        else:
            van_file = f"Van_Urban_{num_clients}.xlsx"
            uav_file = f"Drone_Urban_{num_clients}.xlsx"

        if van_file in files and uav_file in files:
            # Carica le distanze
            distances_truck = load_distances(os.path.join(base_path, van_file))
            distances_uav = load_distances(os.path.join(base_path, uav_file))

            # Per ogni velocità del drone
            for drone_speed in drone_speeds:
                # Esegui l'algoritmo FSTSP con la velocità variabile
                print(f"\nTesting with {num_clients} clients, truck speed: {truck_speed} km/h and drone speed: {drone_speed} km/h")
                
                # Parametri per la funzione fstsp_heuristic
                s_l = 0  # Impostati a 0 per evitare problemi di aggiornamento tempi
                s_r = 0  # Impostati a 0 per evitare problemi di aggiornamento tempi
                e = drone_endurance  # Endurance

                # Prima chiama solveTSP per ottenere il percorso senza l'UAV
                C = list(range(1, num_clients + 1))  # C = {1, 2, ..., n}
                C_prime = C  # Al momento C_prime è uguale a C

                # Chiama solveTSP
                truck_route_tsp, t_tsp = solveTSP(C, distances_truck, truck_speed)

                # Calcola il tempo di consegna con TSP (tempo di ritorno al deposito)
                tsp_delivery_time = t_tsp[0]  # Tempo di ritorno al nodo 0 (depot)
                print(f"Tempo di consegna con TSP (senza UAV): {tsp_delivery_time:.2f} ore")

                # Chiama l'euristica FSTSP
                truck_route_fstsp, t_fstsp = fstsp_heuristic(C, C_prime, distances_truck, truck_speed, e, distances_uav, drone_speed, s_l, s_r)

                # Calcola il tempo di consegna con l'euristica FSTSP (tempo di ritorno al deposito)
                fstsp_delivery_time = t_fstsp[0]  # Tempo di ritorno al nodo 0 (depot)
                print(f"Tempo di consegna con FSTSP (con UAV): {fstsp_delivery_time:.2f} ore")

                # Calcola la percentuale di tempo risparmiato
                time_savings_percent = ((tsp_delivery_time - fstsp_delivery_time) / tsp_delivery_time) * 100

                # Salva i risultati in una lista
                results.append({
                    'num_clients': num_clients,
                    'drone_speed': drone_speed,
                    'tsp_delivery_time': tsp_delivery_time,
                    'fstsp_delivery_time': fstsp_delivery_time,
                    'time_savings_percent': time_savings_percent
                })

                print(f"Finished testing with drone speed: {drone_speed} km/h\n")

    # Stampa finale dei risultati
    print("\n--- Risultati finali ---")
    df_results = pd.DataFrame(results)
    print(df_results)

    # Stampa la tabella con il tempo risparmiato
    print("\n--- Percentuale di tempo risparmiato rispetto a TSP ---")
    df_savings = df_results[['num_clients', 'drone_speed', 'time_savings_percent']]
    print(df_savings)

if __name__ == "__main__":
    analyze_vdrpmdpc_simulation()