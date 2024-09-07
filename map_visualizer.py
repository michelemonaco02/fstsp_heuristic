import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle, FancyArrowPatch
from typing import List, Tuple

def visualize_fstsp(clients: List[Tuple[float, float]], depot: Tuple[float, float], 
                    initial_route: List[int], final_route: List[int], 
                    drone_routes: List[Tuple[int, int, int]]) -> None:
    """
    Visualize the FSTSP solution including initial and final truck routes, and drone routes.
    """
    fig, ax = plt.subplots(figsize=(12, 10))
    
    # Identify served and unserved customers
    served_customers = set(final_route) - {0}  # 0 is the depot
    for drone_route in drone_routes:
        served_customers.update(drone_route)
    all_customers = set(range(1, len(clients) + 1))
    unserved_customers = all_customers - served_customers

    # Plot clients
    for i, (x, y) in enumerate(clients, start=1):
        if i in unserved_customers:
            color = 'red'
            edge_color = 'darkred'
        else:
            color = 'lightgreen'
            edge_color = 'green'
        rect = Rectangle((x-0.02, y-0.02), 0.04, 0.04, fill=True, facecolor=color, edgecolor=edge_color)
        ax.add_patch(rect)
        ax.text(x, y, str(i), ha='center', va='center', fontweight='bold')

    # Plot depot
    ax.scatter(depot[0], depot[1], c='red', marker='o', s=100, label='Depot')
    ax.text(depot[0], depot[1]-0.05, 'Depot', ha='center', va='top', fontweight='bold')

    # Plot routes
    plot_route_with_arrows(ax, clients, depot, initial_route, 'Initial Truck Route', 'green', '->', '--')
    plot_route_with_arrows(ax, clients, depot, final_route, 'Final Truck Route', 'red', '->')
    
    # Plot all drone routes
    for i, drone_route in enumerate(drone_routes):
        plot_route_with_arrows(ax, clients, depot, drone_route, f'Drone Route {i+1}', 'blue', '->', ':')

    # Set labels and title
    ax.set_xlabel('X coordinate')
    ax.set_ylabel('Y coordinate')
    ax.set_title('FSTSP Visualization (Truck and Drone Routes)')
    ax.legend()

    # Adjust plot limits
    all_points = clients + [depot]
    x_min, x_max = min(p[0] for p in all_points), max(p[0] for p in all_points)
    y_min, y_max = min(p[1] for p in all_points), max(p[1] for p in all_points)
    padding = 0.1 * max(x_max - x_min, y_max - y_min)
    ax.set_xlim(x_min - padding, x_max + padding)
    ax.set_ylim(y_min - padding, y_max + padding)

    # Add text to show unserved customers
    if unserved_customers:
        unserved_text = f"Unserved customers: {', '.join(map(str, unserved_customers))}"
        ax.text(0.5, -0.1, unserved_text, ha='center', va='center', transform=ax.transAxes, color='red')

    plt.show()

def plot_route_with_arrows(ax: plt.Axes, clients: List[Tuple[float, float]], 
                           depot: Tuple[float, float], route: List[int], 
                           label: str, color: str, arrow_style: str, 
                           linestyle: str = '-') -> None:
    """
    Helper function to plot a route with arrows on the given axes.
    """
    coordinates = [depot] + [clients[i-1] for i in route if i != 0] + [depot]
    for start, end in zip(coordinates, coordinates[1:]):
        arrow = FancyArrowPatch(start, end, color=color, arrowstyle=arrow_style, 
                                mutation_scale=20, linewidth=1, linestyle=linestyle,
                                label=label)
        ax.add_patch(arrow)
        label = "_nolegend_"  # Only label the first arrow

def generate_coordinates(distances: np.ndarray) -> np.ndarray:
    """
    Generate 2D coordinates from distance matrix using a simple MDS implementation.
    """
    n = distances.shape[0]
    
    # Double center the squared distances
    H = np.eye(n) - np.ones((n, n)) / n
    B = -0.5 * H.dot(distances**2).dot(H)
    
    # Eigendecomposition
    eigvals, eigvecs = np.linalg.eigh(B)
    
    # Sort eigenvalues in descending order
    idx = np.argsort(eigvals)[::-1]
    eigvals = eigvals[idx]
    eigvecs = eigvecs[:, idx]
    
    # Use the top 2 eigenvectors
    return eigvecs[:, :2] * np.sqrt(eigvals[:2])
