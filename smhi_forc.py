import requests
import json
#import RPi.GPIO as GPIO
import time
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "Welcome to the SMHI API!"

@app.route('/data', methods=['GET'])
def get_data():

    url = "https://opendata-download-metfcst.smhi.se/api/category/pmp3g/version/2/geotype/point/lon/18.063240/lat/59.334591/data.json"

    response = requests.get(url)
    data = response.json()

    return jsonify(data)

@app.route('/filterdata', methods=['GET'])
def get_filtered_data():

    url = "https://opendata-download-metfcst.smhi.se/api/category/pmp3g/version/2/geotype/point/lon/18.063240/lat/59.334591/data.json"

    response = requests.get(url)    
    data = response.json()

    # Här definerar vi vilka väder symboler vi vill ha
    desired_wsymb2_snow = {15, 16, 17, 25, 26, 27}
    desired_pcat_snow = {1, 2}
    desired_wysmb2_rain = {7, 8, 9, 10, 11, 18, 19, 20, 21, 22, 23, 24}
    desired_pcat_rain = {2, 3, 4, 5, 6}

    # Här kopplar vi ihop de två listorna
    desired_wsymb2 = desired_wsymb2_snow.union(desired_wysmb2_rain)
    desired_pcat = desired_pcat_snow.union(desired_pcat_rain)

    # Här definerar va de olika variablerna betyder

    pcat_meanings = {
        1: 'none',
        2: 'snow',
        3: 'snow and rain',
        4: 'rain',
        5: 'drizzle',
        6: 'freezing rain',
        7: 'freezing drizzle'
    }

    wsymb2_meanings = {
        1: 'clear sky',
        2: 'nearly clear sky',
        3: 'variable cloudiness',
        4: 'halfclear sky',
        5: 'cloudy sky',
        6: 'overcast',
        7: 'fog',
        8: 'light rain showers',
        9: 'moderate rain showers',
        10: 'heavy rain showers',
        11: 'thunderstorm',
        12: 'light sleet showers',
        13: 'moderate sleet showers',
        14: 'heavy sleet showers',
        15: 'light snow showers',
        16: 'moderate snow showers',
        17: 'heavy snow showers',
        18: 'light rain',
        19: 'moderate rain',
        20: 'heavy rain',
        21: 'thunder',
        22: 'light sleet',
        23: 'moderate sleet',
        24: 'heavy sleet',
        25: 'light snowfall',
        26: 'moderate snowfall',
        27: 'heavy snowfall'
    }
    
    #kanske parameter t? den inenhåller air temperature

    # Här skapar vi en ny lista som bara innehåller de väder symboler vi vill ha
    filtered_data = []

    # Här loopaar vi igenom alla time serier
    for time_series in data.get('timeSeries', []):
        filtered_entry = {'validTime': time_series['validTime'], 'parameters': []}
        for parameter in time_series.get('parameters', []):
            if parameter['name'] == 'Wsymb2' and parameter['values'][0] in desired_wsymb2:
                parameter['meaning'] = wsymb2_meanings.get(parameter['values'][0], "unknown")
                filtered_entry['parameters'].append(parameter)
            elif parameter['name'] == 'pcat' and parameter['values'][0] in desired_pcat:
                parameter['meaning'] = pcat_meanings.get(parameter['values'][0], "unknown")
                filtered_entry['parameters'].append(parameter)
        if filtered_entry['parameters']: 
            filtered_data.append(filtered_entry)
    
    return jsonify(filtered_data)


if __name__ == '__main__':
    app.run(debug=True)



# 13 Rådande väder
# 17 Nederbörd 2 gånger per dygn, 06 och 18
# 27 Lufttemperatur 2 gånger per dygn, 06 och 18






#pcat precipitation category (1=none, 2=snow, 3=snow and rain, 4=rain, 5=drizzle, 6=freezing rain, 7=freezing drizzle)
#wsymb2 är olika väder symboler
#wsymb2 symboler som vi bryrr oss är:
#15 = light snow showers
#16 = moderate snow showers
#17 = heavy snow showers
#25 = light snpwfall
#26 = moderate snowfall
#27 = heavy snowfall