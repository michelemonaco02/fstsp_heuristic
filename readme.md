C = {1,2,...,n} represents the set of all costumers

C_prime denote the subset of customers that may be serviced by the UAV

tau_i_j = time for truck to arrive from i to j
tau_i_j_uav = time for uav // //

s_l = time for launch
s_r = time to recover

e = endurance

t = dizionario con chiave il nodo e valore il tempo di arrivo. Al nodo 0 si associa il valore di ritorno finale.

truckRoute = current route of the truck, inizia e finisce con 0

truckSubRoutes = lista di tuple in cui il primo parametro è la subroute(e.g [0,2,1]) e il secondo parametro è -1 se in quella rotta non viene usato l'UAV, oppure corrisponde al nodo servito da UAV in quella subroute
per esempio: truckSubRoutes = [([0,1,3,2,4],-1),([4,5,9,6,0],7)]
le subroutes in truckSubRoutes devono essere in ordine per facilitare la gestione dei risparmi di tempo
