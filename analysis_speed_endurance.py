import os
import pandas as pd
from data_loader import load_distances, load_parameters
from fstsp_heuristic import fstsp_heuristic
from solveTSP import solveTSP

# Funzione per convertire i parametri in float, rimuovendo unità come 'sec' e 'kg'
def convert_to_float(value):
    if isinstance(value, str):
        return float(value.replace('km', '').replace('min', '').replace('sec', '').replace(' ', '').replace('[', '').replace(']', ''))
    return float(value)

# Funzione per gestire la conversione dei pesi dei clienti
def parse_demand(demand_str):
    return [convert_to_float(x) for x in demand_str.strip('[] kg').split(',')]

def analyze_simulation_speed_endurance():
    # Lista di file da analizzare, separati per scenari urbani e semi-urbani
    files = {
        20: {
            "semi_urban": {
                "van": ["Van_Semi-Urban_20.xlsx"],
                "drone": ["Drone_Semi-Urban_20.xlsx"]
            }
        },
        40: {
            "urban": {
                "van": ["Van_Urban_40.xlsx"],
                "drone": ["Drone_Urban_40.xlsx"]
            },
            "semi_urban": {
                "van": ["Van_Semi-Urban_40.xlsx"],
                "drone": ["Drone_Semi-Urban_40.xlsx"]
            }
        },
        60: {
            "urban": {
                "van": ["Van_Urban_60.xlsx"],
                "drone": ["Drone_Urban_60.xlsx"]
            },
            "semi_urban": {
                "van": ["Van_Semi-Urban_60.xlsx"],
                "drone": ["Drone_Semi-Urban_60.xlsx"]
            }
        },
        100: {
            "urban": {
                "van": ["Van_Urban_100.xlsx"],
                "drone": ["Drone_Urban_100.xlsx"]
            },
            "semi_urban": {
                "van": ["Van_Semi-Urban_100.xlsx"],
                "drone": ["Drone_Semi-Urban_100.xlsx"]
            }
        }
    }

    base_path = 'Data_and_data-description/TELIKA DATA/'
    
    num_clients_list = [20, 40, 60, 100]  # Numero di clienti per l'analisi

    # Velocità costante del truck
    truck_speed = 40  # km/h fisso per il truck


    # Combinazioni di velocità ed endurance in modo che speed * endurance = 20 km
    speed_endurance_combinations = [
        (30, 20 / 30),  # 20 km/h con un'endurance che copre 15 km
        (40, 20 / 40),  # 30 km/h con un'endurance che copre 15 km
        (50, 20 / 50),  # 40 km/h con un'endurance che copre 15 km
        (60, 20 / 60)   # 50 km/h con un'endurance che copre 15 km
    ]

    # Per memorizzare i risultati finali
    results = []

    # Testa tutte le coppie di file van e drone
    for num_clients in num_clients_list:
        demand_category = f'{num_clients} clients'

        # Carica i parametri del drone e del van
        drone_params = load_parameters(os.path.join(base_path, 'Values of parameters for drone routing.xlsx'), demand_category)

        # Se abbiamo 20 clienti, usiamo solo lo scenario semi-urbano
        if num_clients == 20:
            scenarios = ['semi_urban']
        else:
            # Per 40, 60 e 100 clienti, consideriamo sia gli scenari urbani che semi-urbani
            scenarios = ['urban', 'semi_urban']

        # Cicla sugli scenari (urban e semi-urban per 40, 60, 100)
        for scenario_type in scenarios:
            van_files = files[num_clients][scenario_type]["van"]
            drone_files = files[num_clients][scenario_type]["drone"]

            # Esegui le simulazioni
            for van_file in van_files:
                for uav_file in drone_files:
                    if van_file and uav_file:
                        # Carica le distanze
                        distances_truck = load_distances(os.path.join(base_path, van_file))
                        distances_uav = load_distances(os.path.join(base_path, uav_file))

                        # Per ogni combinazione di velocità ed endurance
                        for drone_speed, drone_endurance in speed_endurance_combinations:
                            # Esegui l'algoritmo FSTSP con la velocità variabile e l'endurance
                            print(f"\nTesting with {num_clients} clients, scenario: {scenario_type}, van file: {van_file}, drone file: {uav_file}, truck speed: {truck_speed} km/h, drone speed: {drone_speed} km/h and endurance: {drone_endurance:.2f} ore")
                            
                            # Parametri per la funzione fstsp_heuristic
                            s_l = 0  # Impostati a 0 per evitare problemi di aggiornamento tempi
                            s_r = 0  # Impostati a 0 per evitare problemi di aggiornamento tempi
                            e = drone_endurance  # Endurance variabile

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
                                'scenario_type': scenario_type,
                                'van_file': van_file,
                                'uav_file': uav_file,
                                'drone_speed': drone_speed,
                                'drone_endurance': drone_endurance,
                                'tsp_delivery_time': tsp_delivery_time,
                                'fstsp_delivery_time': fstsp_delivery_time,
                                'time_savings_percent': time_savings_percent
                            })

                            print(f"Finished testing with drone speed: {drone_speed} km/h and endurance: {drone_endurance:.2f} ore\n")

    # Crea DataFrame con i risultati
    df_results = pd.DataFrame(results)

    # Stampa la tabella dei risultati
    print("\n--- Risultati finali ---")
    print(df_results)

    # Stampa la tabella con il tempo risparmiato
    print("\n--- Percentuale di tempo risparmiato rispetto a TSP ---")
    df_savings = df_results[['num_clients', 'scenario_type', 'van_file', 'uav_file', 'drone_speed', 'drone_endurance', 'time_savings_percent']]
    print(df_savings)

if __name__ == "__main__":
    analyze_simulation_speed_endurance()
