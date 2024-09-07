import pandas as pd
import numpy as np
import ast

def load_distances(file_path):
    df = pd.read_excel(file_path, header=None)

    start_row = 2  # Supponendo che le distanze inizino alla riga 2
    start_col = 2  # Supponendo che le distanze inizino alla colonna 2
    
    distances_df = df.iloc[start_row:, start_col:]

    distances_df = distances_df.apply(pd.to_numeric, errors='coerce')
    distances_df.fillna(float('inf'), inplace=True)

    distances_matrix = distances_df.to_numpy()


    return distances_matrix

def parse_demand(demand_str):
    return [int(x) for x in demand_str.strip('[] kg').split(',')]

def strip_units(value):
    if isinstance(value, str):
        return value.split()[0]  # Take only the numeric part
    return value

def load_parameters(file_path, demand_category):
    df = pd.read_excel(file_path)

    # Replace NaN values in the 'Description' column with the last valid value
    df['Description'] = df['Description'].ffill()

    parameters = {}
    demand_values = []

    # Extract parameters from the DataFrame
    for _, row in df.iterrows():
        description = row['Description'].strip()
        category = row['Category'].strip() if pd.notna(row['Category']) else None
        value = row['Values']

        # Handle demand values based on the selected category
        if description == 'demand':
            if category == demand_category:
                # Convert the string to a list of float
                demand_values = [float(x) for x in ast.literal_eval(strip_units(value))]
        else:
            param_key = f"{description}_{category}" if category else description
            parameters[param_key] = strip_units(value)

    # Add demand values to parameters
    if demand_values:
        parameters[f'demand_{demand_category}'] = demand_values
    else:
        raise ValueError(f"No demand values found for category: {demand_category}")

    return parameters

# Esempio di utilizzo:
file_path = 'Data_and_data-description/TELIKA DATA/Values of parameters for drone routing.xlsx'
num_clients = 40
demand_category = f'{num_clients} clients'

drone_params = load_parameters(file_path, demand_category)
print(f"\nDrone Parameters: {drone_params}")
