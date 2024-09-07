import matplotlib.pyplot as plt
import numpy as np

def visualize_fstsp(clients, depot, truck_route):
    """
    Visualize the FSTSP problem and solution.
    
    :param clients: List of (x, y) coordinates for each client
    :param depot: (x, y) coordinate of the depot
    :param truck_route: List of indices representing the truck's route
    """
    # Create a new figure
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # Plot clients
    client_x, client_y = zip(*clients)
    ax.scatter(client_x, client_y, c='blue', label='Clients')
    
    # Plot depot
    ax.scatter(depot[0], depot[1], c='red', marker='s', s=100, label='Depot')
    
    # Plot truck route
    truck_x = [depot[0]]
    truck_y = [depot[1]]
    for i in truck_route:
        if i == 0:
            truck_x.append(depot[0])
            truck_y.append(depot[1])
        elif i <= len(clients):
            truck_x.append(clients[i-1][0])
            truck_y.append(clients[i-1][1])
    truck_x.append(depot[0])
    truck_y.append(depot[1])
    ax.plot(truck_x, truck_y, c='green', label='Truck Route')
    
    # Set labels and title
    ax.set_xlabel('X coordinate')
    ax.set_ylabel('Y coordinate')
    ax.set_title('FSTSP Visualization (Truck Route)')
    
    # Add legend
    ax.legend()
    
    # Show the plot
    plt.show()