# ♻️ Optimizing Waste Management Disposal In Tokyo Trough Graph Theory Application ♻️

# Introduction
Optimizing waste management in Tokyo using graph theory offers a promising approach to improving the efficiency of the city's complex waste disposal system. Given the historical context of Japan's waste management challenges, particularly with its limited land space and growing urban population, Tokyo has adopted a sophisticated system that integrates waste collection, transportation, recycling, and disposal. 

The traditional Japanese philosophy of Mottainai which emphasizes minimizing waste and maximizing the utility of resources has also influenced the development of waste management strategies, such as heat recovery and resource recycling.

# Data Set
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
This code works as part of processing geographical data to solve a problem like the Chinese Postman Problem, which involves finding the optimal route for visiting various locations. The script starts by loading a CSV file (`'CPP_Data.csv'`) into a Pandas DataFrame. It then ensures that any whitespace around the column names is removed and converts the `LATITUDE` and `LONGITUDE` columns into numeric values to avoid errors during calculations. After preparing the data, the program prompts the user to select a specific city area from the dataset.

Once the user selects a city area, the script proceeds to compute an optimal route based on the chosen area using a function like the Chinese Postman Problem (`chinese_postman_problem`). It then calculates the total distance of the optimal route by iterating through the selected locations, retrieving their latitude and longitude, and using a distance calculation function (likely the great-circle distance) to sum the distances between consecutive points.


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
This function is a helper or utility designed to interact with the user, providing them with a list of available city areas from the dataset. It starts by displaying the unique city areas from the 'CITY AREA' column in the provided data, using data['CITY AREA'].unique(). The user is then prompted to select one of these areas by entering the corresponding number.

To handle potential user errors, the function uses a while loop that repeatedly asks for input until a valid response is given. If the user enters a number within the valid range (1 to the number of available areas), the function returns the selected city area. If the user enters a non-numeric value or a number outside the available range, the function catches the error and prompts the user again for a valid choice. This ensures the program only continues with a valid city area selection.

### C.2 Additional Functions 
```py

def get_distance(lat1, lon1, lat2, lon2):
   R = 6371.0
   lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2]) 
   return acos(sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(lon2 - lon1)) * R
```
The `get_distance` function calculates the great-circle distance between two geographical locations based on their latitude and longitude. It begins by defining `R = 6371.0`, which represents the Earth's radius in kilometers. The function then converts the latitude and longitude of both locations from degrees to radians using the ` map(radians, [lat1, lon1, lat2, lon2])` function. This conversion is essential because trigonometric functions like sine and cosine operate in radians, not degrees.

After converting the coordinates, the function uses the spherical law of cosines to compute the central angle between the two points. The formula involves the sine and cosine of the latitudes and the cosine of the difference in longitudes. The result of this calculation gives the angular distance in radians, which is then multiplied by the Earth's radius (`R`) to obtain the actual distance between the two points in kilometers. This method assumes the Earth is a perfect sphere, providing a simplified yet effective way to calculate the shortest distance over the Earth's surface between any two points.
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
The Chinese postman problem code begins by filtering the dataset to focus on the rows corresponding to the selected `city_area`. If no data is available for the chosen area, the function returns a message indicating that no data is present. Otherwise, it extracts the names of the areas and their respective coordinates (latitude and longitude) into separate lists. These lists are then used to compute the pairwise distances between all areas within the selected city.

The function calculates the distance between each pair of areas using the get_distance function, which computes the great-circle distance between two geographical points. These distances are stored in a dictionary, with both `(name1, name2)` and `(name2, name1)` as keys to account for both directions of travel.

Next, the function selects a random starting node (area) from the available area names. The route list is initialized with this starting area, which will later be used to construct the optimal route for visiting all areas, potentially by applying an algorithm to solve the Chinese Postman Problem, though the route-building logic is not fully included in this snippet.

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

First, the Djisktra code retrieves the latitude and longitude of the `start_vertex` (the starting area) by searching for the corresponding values in the `data` dataset. This is done using the area name (`start_vertex`) and extracting the latitude and longitude from the dataset.

Next, the function filters the list of `incinerationPlants` to include only those of the specified `plant_type`. This creates a subset of plants that match the desired type, narrowing down the search.

The function then initializes two variables: `closest_plant`, which will store the name of the closest plant, and `min_distance`, set initially to infinity to ensure that the first distance calculated will be smaller.

Using a loop, the function iterates through the filtered plants, calculating the distance from the starting point to each plant using the `get_distance` function. If a plant's distance is smaller than the current `min_distance`, the `closest_plant` and `min_distance` are updated to reflect the new closest plant and its distance.

This code doesn't fully implement Dijkstra's algorithm, but it uses the basic idea of calculating the shortest distance from a start point to a target (in this case, a plant) by comparing distances and updating the closest target. It would be part of a larger system that finds the shortest path in a network of points, like the shortest route to a plant-based on distance.
