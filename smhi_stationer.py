import requests
from tabulate import tabulate
import smhi_try
#import RPi.GPIO as GPIO
import os
import tkinter as tk
from tkinter import ttk


param_data = []
stations_data = []
cities = []

username = "kevin125sh"

def param_input_loop():
    global param_data
    
    while(True):
        paramNumber = (input("Enter parameter number: "))
        paramMatch = False


        for param in param_data:
                if param['key'] == paramNumber:
                    print("Parameter found, title:", {param['title']})
                    paramFound = True
                    break

        if not paramMatch:
            print("Parameter not found with the given number") 

def city_input_loop():
    global stations_data
    global cities

    while(True):
        stadName = input("Ange staden du befinner dig i:")
        stadMatch = False
        lat, lon = get_city_coords(stadName)
        if lat is not None and lon is not None:
            print("Stad hittad i databasen cities:")
            table_data = [[stadName, lat, lon]]
            headers = ["Stad", "Latitud", "Longitud"]
            print(tabulate(table_data, headers=headers, tablefmt='pretty'))
            stadMatch = True
            return lat, lon
            
        
        elif lat is None and lon is None:
            lat, lon = get_station_coords(stadName)
            if lat is not None and lon is not None:
                print("Stad hittad i databasen stations:", stadName)
                table_data = [[stadName, lat, lon]]
                headers = ["Stad", "Latitud", "Longitud"]
                print(tabulate(table_data, headers=headers, tablefmt='pretty'))
                stadMatch = True
                return lat, lon
       
        if not stadMatch:
            print("Stad ej hittad i databasen:", stadName)

def get_city_coords(city_name):
    global cities
    for city in cities:
        if city.get('toponmymName','').lower() == city_name.lower():
            return city.get('lat'), city.get('lng')
    return None, None

def get_station_coords(station_name):
    for station in stations_data:
        if station.get('name','').lower() == station_name.lower():
            return station.get('latitude'), station.get('longitude')
    return None, None

def fetch_cities():
    global cities

    geoname_url = "http://api.geonames.org/searchJSON?q=&country=SE&featureClass=P&maxRows=1000&username=kevin125sh"
    response = requests.get(geoname_url)
   
    data = response.json()
    
    for elememt in data['geonames']:
        city_name = elememt.get('toponymName')
        city_id = elememt.get('adminCode1')
        city_lat = elememt.get('lat')
        city_lon = elememt.get('lng')
        cities.append({'toponmymName': city_name, 'id': city_id, 'lat': city_lat, 'lng': city_lon})
    
    return cities

def fetch_parameters():
    global param_data

    url = "https://opendata-download-metobs.smhi.se/api/version/1.0/parameter.json"

    response = requests.get(url)
    
    if response.status_code == 200:

        parameter_data = response.json()
        param_data = parameter_data.get('resource', [])

        for param in param_data:
            print(param['key'])
            print(param['title'])
            print(param['summary'])
            """ 
            print(param['updated'])
            print(param['title'])
            print(param['summary'])
            print(param['unit'])  """
            print('-' * 20) 
        
    else: 
        print(f'Error fetching data, error code:', {response.status_code}) 

def fetch_stations(): 
    global stations_data

    url = "https://opendata-download-metobs.smhi.se/api/version/1.0/parameter/1/station.json"

    response = requests.get(url)

    if response.status_code == 200:
        
        data = response.json()
        stations_data = data.get('station', [])  

        """ for station in stations_data:
            print(station['name'])
            print(station['id'])
            print(station['latitude'])
            print(station['longitude'])
            print(station['height'])
            print(station['active'])
            print('-' * 20) """
    else:
        print(f'Error fetching data, error code:', {response.status_code})  

def clear_terminal():
    # For Windows
    if os.name == 'nt':
        os.system('cls')

    # For Mac and Linux(here, os.name is 'posix')
    else:
        os.system('clear')

if __name__ == '__main__':

    fetch_stations()
    #fetch_parameters()
    #param_input_loop()
    fetch_cities()
    clear_terminal()
    lat, lon = city_input_loop()
    smhi_try.main(lat, lon)
    

'''
 13 Rådande väder
 17 Nederbörd 2 gånger per dygn, 06 och 18
 27 Lufttemperatur 2 gånger per dygn, 06 och 18

'''