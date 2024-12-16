import os
import json
import folium
import streamlit as st

from streamlit_folium import st_folium

import folium

def openJson(path):
    
    with open(path, 'r') as json_file:
        json_dict = json.load(json_file)
    return json_dict

def getTravelCoordinates(db):
    
    coords = []
    cities_list = db["cityList"]
    for city in cities_list:
        city_dict = db[city]
        coords.append([city_dict["Lat"], city_dict["Lon"]])
    return coords

def createTravel(travel_dict):
    
    travel_dir = os.path.join('travels', travel_dict["folder"])
    travel_db_path = os.path.join(travel_dir, 'travelDatabase.json')
    with open('temp.log', 'w') as temp_log:
        temp_log.write(travel_db_path)
        temp_log.close()
    travel_db = openJson(travel_db_path)
    travel_coordinates = getTravelCoordinates(travel_db)
    travel = folium.FeatureGroup(name=travel_dict["name"])
    folium.PolyLine(travel_coordinates, color="blue", weight=5, opacity=0.8).add_to(travel)
    return travel

def main():

    m = folium.Map(location=[54.5260, 15.2551], zoom_start=4)
    
    travels_db = openJson('mapDatabase.json')
    
    for key_travel, travel in travels_db.items():
        travel = createTravel(travel)
        travel.add_to(m)
    
    folium.LayerControl().add_to(m)
    m.save('myMap.html')
    #st_data = st_folium(m, width=725)

if __name__ == "__main__":
    main()


"""# Deuxième trajet : Londres -> Amsterdam -> Rome
trajet_2 = folium.FeatureGroup(name="Trajet 2 : Londres - Amsterdam - Rome")
coordinates_2 = [
    [51.5074, -0.1278],  # Londres
    [52.3676, 4.9041],   # Amsterdam
    [41.9028, 12.4964],  # Rome
]
folium.PolyLine(
    coordinates_2, color="green", weight=5, opacity=0.8
).add_to(trajet_2)

for coord, city in zip(coordinates_2, ["Londres", "Amsterdam", "Rome"]):
    folium.Marker(
        location=coord,
        popup=f"<b>{city}</b>",
        icon=folium.Icon(color="green", icon="info-sign")
    ).add_to(trajet_2)"""