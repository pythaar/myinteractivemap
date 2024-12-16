import requests
import json
import sys
import os

def createJsonIfNot(file_path):
    
    json_dict = {}
    if not os.path.exists(file_path):
        with open(file_path, 'w') as json_file:
            json.dump(json_dict, json_file)

def makeRequest(city_name):
    
    public_db_url = "https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/geonames-all-cities-with-a-population-1000/records?"
    request_params = {"where": f"name = '{city_name}' OR ascii_name = '{city_name}' OR '{city_name}' IN alternate_names", "limit":100}
    request = requests.get(public_db_url, params=request_params)
    if request.status_code == 200:
        if request.json()["total_count"] == 0:
            print(city_name + ' ignored: no city found')
            return []
        else:
            return request.json()["results"]
    else:
        print(city_name + ' ignored: error in request')
        return []
         
def chooseCity(request):
    
    for i_city, city in enumerate(request):
         print(str(i_city) + ": " + city["name"] + ", " + city["cou_name_en"])
    
    idx_city = int(input("Choose city by index, -1 for detailed coordinates: "))
    if 0<=idx_city<len(request):
        return [request[idx_city]]
    elif idx_city == -1:
        for i_city, city in enumerate(request):
            print(str(i_city) + ": " + city["name"] + ", " + city["cou_name_en"] + ', ' + str(city["coordinates"]["lat"]) + ', ' + str(city["coordinates"]["lon"]))
        idx_city = int(input("Choose city by index: "))
        if 0<=idx_city<len(request):
            return [request[idx_city]]
        else:
            print(city["name"] + ' ignored: wrong index')
            return []
    else:
        print(city["name"] + ' ignored: wrong index')
        return []
         
         
def getCity(city_name):
    
    request = makeRequest(city_name)
    if request:
        if len(request) > 1:
            return chooseCity(request)
        else:
            return request
    else:
        return []
    
    

def getCitiesCoordinates(inputs, database):
    
    if "cityList" in database:
        city_list = database["cityList"]
    else:
        city_list = []
    for line in inputs:
        city_name = line.strip()
        city = getCity(city_name)  
        if city:
            database[city[0]["ascii_name"]] = {"Country": city[0]["cou_name_en"], "Lon":city[0]["coordinates"]["lon"], "Lat":city[0]["coordinates"]["lat"]}
            city_list.append(city[0]["ascii_name"])
    database["cityList"] = city_list
    
    return database

def main():
    
    args = sys.argv
    workdir = args[-1]
    raw_travel_path = os.path.join(workdir, 'rawTravel.txt')
    if not os.path.exists(raw_travel_path):
        sys.exit(raw_travel_path + ' does not exists')
    
    with open(raw_travel_path, 'r') as raw_file:
        lines = raw_file.readlines()
    
    travel_db_path = os.path.join(workdir, 'travelDatabase.json')
    createJsonIfNot(travel_db_path)
    with open(travel_db_path, 'r') as travel_db_file:
        travel_db = json.load(travel_db_file)
        
    travel_db = getCitiesCoordinates(lines, travel_db)
    with open(travel_db_path, 'w') as travel_db_file:
        json.dump(travel_db, travel_db_file)
    

if __name__ == "__main__":
    main()
