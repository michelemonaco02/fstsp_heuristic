import matplotlib.pyplot as plt
import numpy as np

def visualize_fstsp(clients, depot, initial_route, final_route, drone_route):
    """
    Visualize the FSTSP problem and solution.
    
    :param clients: List of (x, y) coordinates for each client
    :param depot: (x, y) coordinate of the depot
    :param initial_route: List of indices representing the initial truck's route
    :param final_route: List of indices representing the final truck's route
    :param drone_route: List of indices representing the drone's route
    """
    fig, ax = plt.subplots(figsize=(12, 10))
    
    client_x, client_y = zip(*clients)
    ax.scatter(client_x, client_y, c='blue', label='Clients')
    ax.scatter(depot[0], depot[1], c='red', marker='s', s=100, label='Depot')
    
    plot_route(ax, clients, depot, initial_route, 'Initial Truck Route', 'green', '--')
    plot_route(ax, clients, depot, final_route, 'Final Truck Route', 'red', '-')
    plot_route(ax, clients, depot, drone_route, 'Drone Route', 'purple', ':')
    
    ax.set_xlabel('X coordinate')
    ax.set_ylabel('Y coordinate')
    ax.set_title('FSTSP Visualization (Truck and Drone Routes)')
    ax.legend()
    plt.show()

def plot_route(ax, clients, depot, route, label, color, linestyle):
    """Helper function to plot a route"""
    x = [depot[0]]
    y = [depot[1]]
    for i in route:
        if i == 0:
            x.append(depot[0])
            y.append(depot[1])
        elif i <= len(clients):
            x.append(clients[i-1][0])
            y.append(clients[i-1][1])
    x.append(depot[0])
    y.append(depot[1])
    ax.plot(x, y, c=color, linestyle=linestyle, label=label)

# Example usage
if __name__ == "__main__":
    clients = [(1, 1), (2, 4), (3, 2), (5, 3), (6, 1), (4, 5), (2, 6), (1, 3)]
    depot = (0, 0)
    initial_route = [0, 1, 2, 3, 4, 5, 7, 6, 8, 0]
    final_route = [0, 1, 2, 3, 4, 5, 7, 6, 0]
    drone_route = [0, 8, 1]
    
    visualize_fstsp(clients, depot, initial_route, final_route, drone_route)