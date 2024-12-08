# ⋆｡‧˚ʚ🗑️ɞ˚‧｡⋆ Optimizing Waste Management Disposal In Tokyo Trough Graph Theory Application

# Introduction
Optimizing waste management in Tokyo using graph theory offers a promising approach to improving the efficiency of the city's complex waste disposal system. Given the historical context of Japan's waste management challenges, particularly with its limited land space and growing urban population, Tokyo has adopted a sophisticated system that integrates waste collection, transportation, recycling, and disposal. 

The traditional Japanese philosophy of Mottainai which emphasizes minimizing waste and maximizing the utility of resources has also influenced the development of waste management strategies, such as heat recovery and resource recycling.

# DataSet
In collecting the dataset, we prioritised finding relevant and reliable resources. Once identified, we then used Google Maps to determine the longitude and latitude of each location. 

## Data for Chinese Postman Problem (CPP)

   <img width="480" alt="Screenshot 2024-12-08 at 6 55 57 PM" src="https://github.com/user-attachments/assets/2d2c07f2-1420-49a6-9e67-7122e4839699">


The dataset required for the CPP Algorithm includes the area name in which the garbage collection edge is located, accompanied by the city name that the area is in and its respective longitude and latitude points. The data acquired has been obtained from the Gomi-Map Application; A Japan-based app that uses data and technology to promote sustainability. It helps users find nearby recycling spots and the best routes to navigate towards the recycling spot. 


## Data for Dijkstra

   <img width="480" alt="Screenshot 2024-12-08 at 6 56 18 PM" src="https://github.com/user-attachments/assets/1f66a5a1-992e-44bd-afc4-78535e551828">


The dataset required for the Dijkstra Algorithm includes the various types of incineration plants located in Tokyo. To accommodate the algorithm’s need for searching the closest incineration plant depending on the specific type of incineration plant needed to travel to, we have attained information based on the Waste Report 2023 by the Clean Authority of Tokyo and categorized the locations to mainly two primary types: one for combustible materials, and another for incombustible materials. Additionally, for cases involving recycling, we’ve added information based on a report made by ShinMaywa Industries, Ltd. to ensure that the dataset is able to include relevant recycling centers as alternative destinations.

# Codes
### A. Libraries
```py

import pandas as pd
import networkx as nx
import random
import math
import heapq
from collections import namedtuple
from math import acos, sin, cos, radians

```


### B. Main Function
```py

if __name__ == "__main__":
   data = pd.read_csv('CPP_Data.csv', delimiter=",")
  
   data.columns = data.columns.str.strip()
   # Ensure LATITUDE and LONGITUDE are numeric
   data['LONGITUDE'] = pd.to_numeric(data['LONGITUDE'], errors='coerce')
   data['LATITUDE'] = pd.to_numeric(data['LATITUDE'], errors='coerce')
  
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


   print ("\n")
   print("Optimal route: ", optimal_route)
   print("\nTotal distance of the optimal route:", total_distance)
   print ("\n")
   print(f"The closest incineration plant of type {dijkstra_type} to the last area in the optimal route is {final_incinerationPlant} with a distance of {final_distance} km.")
```

### C.1 Additional Functions 
```py

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
```

### C.2 Additional Functions 
```py

def get_distance(lat1, lon1, lat2, lon2):
   R = 6371.0
   lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2]) 
   return acos(sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(lon2 - lon1)) * R
```

## Code for Chinese Postman Problem
```py

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
```

## Code for Dijkstra 
```py

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

```
