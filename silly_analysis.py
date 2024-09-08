from fstsp_heuristic import fstsp_heuristic
from solveTSP import solveTSP
import random

# Numero di clienti
n_customers = 20

# Lista dei nodi, C, che rappresenta i clienti (dal nodo 1 a n_customers)
C = [i for i in range(1, n_customers + 1)]

# C_prime è la stessa cosa di C
C_prime = C

# Velocità del truck e del drone
truck_speed = 60  # in km/h
uav_speed = 100   # in km/h

# Tempo massimo che il drone può volare (in ore)
e = 0.5  # tempo massimo volo drone in ore (e.g., 30 minuti)

# Tempo di lancio e retrieval del drone
s_l = 0  # in ore
s_r = 0  # in ore

# Funzione per generare una matrice simmetrica delle distanze
def generate_symmetric_matrix(n, min_val, max_val):
    matrix = [[0 if i == j else random.randint(min_val, max_val) for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            matrix[j][i] = matrix[i][j]
    return matrix

# Genera una matrice delle distanze simmetriche per il truck (distanze in km)
distances_truck = generate_symmetric_matrix(n_customers + 1, 30, 150)

# Genera una matrice delle distanze simmetriche per l'UAV (distanze in km)
distances_uav = generate_symmetric_matrix(n_customers + 1, 10, 80)

# Stampa le matrici di distanze del truck
print("Matrice delle distanze del truck (km):")
for row in distances_truck:
    print(row)

# Stampa le matrici di distanze dell'UAV
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
