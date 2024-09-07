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
wa = HydrometricStations(stn_id=stations)
# for a dictionary of dataframes
dcf = wa.to_dict_frame()
# for an xarray
ds = wa.to_xr()
```
You can also pass the bbox argument to get all the stations within the boundary box.

For weather stations, you can also invoke the `plot_stations()` method:
```python
from weather_api import WeatherStations

ws = WeatherStations()
ws.plot_stations()
```

![map](images/map_weather.png)

You can interact with the map and find out which station ids you need. For this example, we extract two stations from Toronto, ON.
```python
stations = ["6158350", "6158355"]
wa = WeatherStations(stn_id=stations)
ds = wa.to_xr()
ds
```
![xarray](images/xarray.png)

One of these stations is from 1840-2002 and the other is from 2002-Current. We can combine these stations:
```python
temp = ds['MEAN_TEMPERATURE']
combined = temp.sel(climate_identifier=stations[0])
combined = combined.combine_first(temp.sel(climate_identifier=stations[1]))
combined.plot()
```
![temperature](images/temperature.png)