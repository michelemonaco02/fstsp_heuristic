import random
from fstsp_heuristic import fstsp_heuristic
from solveTSP import solveTSP

# Numero di clienti
n_customers = 5

# Lista dei nodi, C, che rappresenta i clienti (dal nodo 1 a n_customers)
C = [i for i in range(1, n_customers + 1)]

# C_prime è la stessa cosa di C
C_prime = C

# Velocità del truck e del drone (arbitrario)
truck_speed = 60  # in km/h
uav_speed = 100   # in km/h

# Tempo massimo che il drone può volare (in ore)
e = 0.5  # tempo massimo volo drone in ore (e.g., 30 minuti)

# Tempo di lancio e retrieval del drone
s_l = 0.1  # in ore
s_r = 0.1  # in ore

# Generiamo una matrice delle distanze casuale per il truck (distanze in km)
distances_truck = [[0 if i == j else random.randint(10, 50) for j in range(n_customers + 1)] for i in range(n_customers + 1)]

# Generiamo una matrice delle distanze casuale per l'UAV (distanze in km)
distances_uav = [[0 if i == j else random.randint(5, 30) for j in range(n_customers + 1)] for i in range(n_customers + 1)]

# Stampa le matrici di distanze generate
print("Matrice delle distanze del truck (km):")
for row in distances_truck:
    print(row)

print("\nMatrice delle distanze dell'UAV (km):")
for row in distances_uav:
    print(row)

# Chiama solveTSP per ottenere il percorso del truck senza l'UAV
truck_route_tsp, t_tsp = solveTSP(C, distances_truck, truck_speed)

# Stampa il percorso e i tempi iniziali del truck
print("\nPercorso del truck con solveTSP (senza UAV):")
print(truck_route_tsp)

print("\nTempi di arrivo ai nodi (solveTSP):")
for node, arrival_time in t_tsp.items():
    print(f"Nodo {node}: {arrival_time:.2f} ore")

# Chiama l'euristica FSTSP
truck_route_fstsp, t_fstsp = fstsp_heuristic(C, C_prime, distances_truck, truck_speed, e, distances_uav, uav_speed, s_l, s_r)

# Stampa i risultati dell'heuristica FSTSP
print("\nPercorso del truck con fstsp_heuristic:")
print(truck_route_fstsp)

print("\nTempi di arrivo ai nodi (fstsp_heuristic):")
for node, arrival_time in t_fstsp.items():
    print(f"Nodo {node}: {arrival_time:.2f} ore")
