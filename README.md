# Rain Forecast

A Python-based weather application that uses SMHI's open weather APIs to check whether rain is expected for a selected Swedish city.

The project started as a weather/IoT experiment and combines a Tkinter desktop interface, SMHI forecast data, Swedish city/station lookup, and a Flask API. The code also contains prepared Raspberry Pi GPIO functionality for using the forecast to control LEDs or other hardware.


## Features

- Search for a Swedish city through a Tkinter desktop interface.
- Resolve the selected city's latitude and longitude.
- Fall back to SMHI weather-station coordinates when needed.
- Retrieve forecast data from SMHI's open Meteorological Forecast API.
- Detect rain and precipitation using SMHI's `Wsymb2` and `pcat` parameters.
- Display the nearest relevant rain forecast.
- Check whether rain is expected within approximately the next hour.
- Refresh the forecast automatically every hour.
- Provide a Flask API for exposing SMHI weather data and filtered precipitation data.
- Includes prepared Raspberry Pi GPIO/LED logic for future hardware integration.

## How it works

The application follows this general flow:

```text
User enters city
       │
       ▼
City / station lookup
       │
       ▼
Latitude + longitude
       │
       ▼
SMHI Forecast API
       │
       ▼
Filter Wsymb2 + pcat
       │
       ├── Rain detected
       │      │
       │      ▼
       │   Find nearest rain forecast
       │      │
       │      ▼
       │   Display status / time
       │
       └── No rain detected
              │
              ▼
          STBY status
```

The main application uses `interface.py`, while the weather retrieval and rain-detection logic is handled primarily by `smhi_try.py`.

## Project structure

```text
Rain-forecast/
├── interface.py          # Tkinter desktop interface
├── smhi_try.py           # Forecast retrieval and rain detection
├── smhi_stationer.py     # City/station lookup and SMHI station data
├── smhi_forc.py          # Flask API for weather data
├── requirements.txt      # Python dependencies
├── interface.spec        # PyInstaller build configuration
├── build/                # PyInstaller build output
├── dist/                 # Built application output
├── .flaskenv             # Flask environment configuration
├── .gitignore
└── LICENSE
```

## Requirements

- Python 3
- Internet connection
- Tkinter
- Python packages listed in `requirements.txt`
- Access to the SMHI open data APIs
- GeoNames access for the city lookup functionality

For Raspberry Pi hardware functionality, a compatible Raspberry Pi and GPIO support are also required.

## Installation

Clone the repository:

```bash
git clone git@github.com:Kev1nSh/Rain-forecast.git
cd Rain-forecast
```

Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Run the desktop application

Start the Tkinter interface with:

```bash
python3 interface.py
```

Enter a Swedish city and press **Submit** or **Enter**.

The application will:

1. Look up the city coordinates.
2. Request the forecast from SMHI.
3. Analyze precipitation-related forecast parameters.
4. Display whether rain is expected and the relevant forecast time.
5. Continue updating the forecast approximately every hour.

## Flask API

`smhi_forc.py` contains a small Flask application that exposes weather data through HTTP endpoints.

Start it with:

```bash
python3 smhi_forc.py
```

Available endpoints include:

```text
GET /
GET /data
GET /filterdata
```

`/data` returns raw forecast data from SMHI, while `/filterdata` returns data filtered around precipitation-related `Wsymb2` and `pcat` values.

> Note: The current Flask implementation contains a fixed Stockholm coordinate in its API URL. The desktop application, however, passes the selected city's coordinates dynamically to the SMHI forecast API.

## Rain detection

The project uses two SMHI forecast parameters:

### `Wsymb2`

`Wsymb2` represents the weather symbol/condition, including different types and intensities of rain, snow, sleet and thunderstorms.

The current rain-detection logic focuses on values representing conditions such as:

- Light rain showers
- Moderate rain showers
- Heavy rain showers
- Light rain
- Moderate rain
- Heavy rain

### `pcat`

`pcat` represents the precipitation category.

The application currently considers selected precipitation categories including:

- Snow and rain
- Rain
- Freezing rain

The two parameters are used together to identify relevant precipitation events.

## Raspberry Pi / IoT integration

The project contains prepared GPIO functionality intended for Raspberry Pi hardware.

The intended concept is:

```text
SMHI forecast
     │
     ▼
Rain within ~1 hour?
   ┌─┴─┐
  YES  NO
   │    │
   ▼    ▼
 PWR   STBY
 ON
```

The GPIO code is currently commented out, so the project can be run without Raspberry Pi hardware.

## Building the desktop application

The repository contains `interface.spec`, which can be used with PyInstaller.

For example:

```bash
pyinstaller interface.spec
```

The generated files are placed in the `build/` and `dist/` directories.

## Data sources

This project uses:

- **SMHI Open Data** for weather forecasts and weather-station information.
- **GeoNames** for Swedish city lookup.

The project depends on these external services being available and reachable from the machine running the application.

## Notes

This repository is primarily a learning and development project combining:

- Python
- REST APIs
- GUI development with Tkinter
- Flask
- JSON data processing
- Weather-data filtering
- Location lookup
- Raspberry Pi / GPIO concepts
- Basic IoT automation

Some parts of the project are experimental or prepared for future hardware integration.

## License

This project is licensed under the MIT License. See [`LICENSE`](LICENSE) for details.
