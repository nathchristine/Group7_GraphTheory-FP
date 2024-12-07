import pandas as pd
import networkx as nx
import random
import math
import heapq
from collections import namedtuple
from math import acos, sin, cos, radians

def get_distance(lat1, lon1, lat2, lon2):
    R = 6371.0 
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])  
    return acos(sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(lon2 - lon1)) * R

def get_city_area(data):
    print("Available city areas:")
    city_areas = data['CITY AREA'].unique()
    for idx, area in enumerate(city_areas, 1):
        print(f"{idx}. {area}")
    
    while True:
        try:
            choice = int(input("Enter the number of your selected city area: "))
            if 1 <= choice <= len(city_areas):
                return city_areas[choice - 1]
            else:
                print("Invalid choice. Please select a valid number.")
        except ValueError:
            print("Please enter a valid number.")

def chinese_postman_problem(city_area, data):
    filtered_data = data[data['CITY AREA'] == city_area]
    
    if filtered_data.empty:
        return f"No data available for the selected city area: {city_area}."
    
    area_names = filtered_data['AREA NAME'].tolist()
    coordinates = filtered_data[['LATITUDE', 'LONGITUDE']].values.tolist()
    
    distances = {}
    for i, (name1, (lat1, lon1)) in enumerate(zip(area_names, coordinates)):
        for j, (name2, (lat2, lon2)) in enumerate(zip(area_names, coordinates)):
            if i < j:  
                distance = get_distance(lat1, lon1, lat2, lon2)
                distances[(name1, name2)] = distance
                distances[(name2, name1)] = distance  
    
    start_node = random.choice(area_names)
    
    route = [start_node]
    visited_nodes = {start_node}
    
    current_node = start_node
    while len(visited_nodes) < len(area_names):
        nearest_node = None
        min_distance = float('inf')
        
        for (node1, node2), distance in distances.items():
            if node1 == current_node and node2 not in visited_nodes:
                if distance < min_distance:
                    nearest_node = node2
                    min_distance = distance
        
        if nearest_node:
            route.append(nearest_node)
            visited_nodes.add(nearest_node)
            current_node = nearest_node
    
    return route

df = pd.read_csv('data dijkstra.csv')

incinerationPlant = namedtuple('incinerationPlant', ['name', 'type', 'longitude', 'latitude'])

incinerationPlants = [
    incinerationPlant(name, type, longitude, latitude)
    for name, type, longitude, latitude in zip(
        df['Name'], df['Type'], df['Longitude'], df['Latitude']
    )
]

incinerationPlant_types = df['Type'].unique()

def dijkstra(start_vertex, plant_type):
    start_lat, start_lon = data[data['AREA NAME'] == start_vertex][['LATITUDE', 'LONGITUDE']].values[0]

    filtered_plants = [
        plant for plant in incinerationPlants if plant.type == plant_type
    ]

    closest_plant = None
    min_distance = float('inf')

    for plant in filtered_plants:
        distance = get_distance(start_lat, start_lon, plant.latitude, plant.longitude)
        if distance < min_distance:
            closest_plant = plant.name
            min_distance = distance

    return closest_plant, min_distance


if __name__ == "__main__":
    data = pd.read_csv('cpp.csv', delimiter=";")
    
    data['LONGITUDE'] = data['LONGITUDE'].str.replace(',', '.').astype(float)
    data['LATITUDE'] = data['LATITUDE'].str.replace(',', '.').astype(float)
    
    city_area = get_city_area(data)
    
    optimal_route = chinese_postman_problem(city_area, data)
    total_distance = 0
    for i in range(len(optimal_route) - 1):
        lat1, lon1 = data[data['AREA NAME'] == optimal_route[i]][['LATITUDE', 'LONGITUDE']].values[0]
        lat2, lon2 = data[data['AREA NAME'] == optimal_route[i + 1]][['LATITUDE', 'LONGITUDE']].values[0]
        total_distance += get_distance(lat1, lon1, lat2, lon2)
    
    start_vertex = optimal_route[-1]
    
    print("Available incineration plant type: ")
    for i, plant_type in enumerate(incinerationPlant_types):
        print(f"{i + 1}: {plant_type}")
     
    print("Enter the number of your selected incineration plant type: ", end="")
    type_index = input()
    dijkstra_type = incinerationPlant_types[int(type_index) - 1]
    
    final_incinerationPlant, final_distance = dijkstra(start_vertex, dijkstra_type)
    
    print("Optimal route:", optimal_route)
    print("Total distance of the optimal route:", total_distance)
    print(f"The closest incineration plant of type {dijkstra_type} to the last area in the optimal route is {final_incinerationPlant} with a distance of {final_distance} km.")
