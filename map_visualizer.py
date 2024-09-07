import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle, FancyArrowPatch

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
    
    # Plot clients as green rectangles with numbers
    for i, (x, y) in enumerate(clients, start=1):
        rect = Rectangle((x-0.02, y-0.02), 0.04, 0.04, fill=True, facecolor='lightgreen', edgecolor='green')
        ax.add_patch(rect)
        ax.text(x, y, str(i), ha='center', va='center', fontweight='bold')

    # Plot depot as a red circle with legend
    ax.scatter(depot[0], depot[1], c='red', marker='o', s=100, label='Depot')
    ax.text(depot[0], depot[1]-0.05, 'Depot', ha='center', va='top', fontweight='bold')

    # Plot routes with arrows
    plot_route_with_arrows(ax, clients, depot, initial_route, 'Initial Truck Route', 'green', '->', '--')
    plot_route_with_arrows(ax, clients, depot, final_route, 'Final Truck Route', 'red', '->')
    plot_route_with_arrows(ax, clients, depot, drone_route, 'Drone Route', 'blue', '->')

    # Set labels and title
    ax.set_xlabel('X coordinate')
    ax.set_ylabel('Y coordinate')
    ax.set_title('FSTSP Visualization (Truck and Drone Routes)')
    ax.legend()

    # Adjust the plot limits
    all_points = clients + [depot]
    x_min, x_max = min(p[0] for p in all_points), max(p[0] for p in all_points)
    y_min, y_max = min(p[1] for p in all_points), max(p[1] for p in all_points)
    padding = 0.1 * max(x_max - x_min, y_max - y_min)
    ax.set_xlim(x_min - padding, x_max + padding)
    ax.set_ylim(y_min - padding, y_max + padding)

    plt.show()

def plot_route_with_arrows(ax, clients, depot, route, label, color, arrow_style, linestyle='-'):
    """Helper function to plot a route with arrows"""
    coordinates = [depot] + [clients[i-1] for i in route if i != 0] + [depot]
    for start, end in zip(coordinates, coordinates[1:]):
        arrow = FancyArrowPatch(start, end, color=color, arrowstyle=arrow_style, 
                                mutation_scale=20, linewidth=1, linestyle=linestyle,
                                label=label)
        ax.add_patch(arrow)
        label = "_nolegend_"  # Only label the first arrow
