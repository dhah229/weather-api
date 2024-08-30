# weather-api
![Tests](https://github.com/dhah229/weather-api/actions/workflows/tests.yml/badge.svg)


This is a Python package that provides a convenient way to fetch weather station and hydrometric station data using the GeoMet OGC API. It simplifies the process of retrieving data and parsing it into pandas DataFrames or xarray datasets for further analysis.

## Installation
Clone the library and run (editable)
```
pip install -e .
```

## Usage
Here's a basic example of how to use the weather-api to fetch and parse the hydrometric station data:
```python
from weather_api import HydrometricStations

stations = ['05MH001', '05MH006', '05MJ001']
hs = HydrometricStations(stn_id=stations)
# for a dictionary of dataframes
d_f = hs.to_dict_frame()
# for an xarray
ds = hs.to_xr()
```
You can also pass the bbox argument to get all the stations within the boundary box.

For weather stations, you can also invoke the `plot_stations()` method:
```python
from weather_api import WeatherStations

ws = WeatherStations()
ws.plot_stations()
```
You can interact with the map and find out which station ids you need.