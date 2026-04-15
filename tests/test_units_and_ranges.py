from datetime import datetime

import pytest
import xarray as xr

from weather_api import HydrometricStations, WeatherStations


def test_weather_units_and_ranges():
    station = "6158355"
    wa = WeatherStations(stn_id=station, start_date=datetime(2020, 1, 1), end_date=datetime(2020, 1, 10))
    ds = wa.to_xr()
    # Check units and reasonable ranges for some variables
    if "MEAN_TEMPERATURE" in ds:
        assert ds["MEAN_TEMPERATURE"].attrs.get("units") == "degC"
        # Typical range for air temperature in Canada
        assert ds["MEAN_TEMPERATURE"].min() > -60
        assert ds["MEAN_TEMPERATURE"].max() < 60
    if "TOTAL_PRECIPITATION" in ds:
        assert ds["TOTAL_PRECIPITATION"].attrs.get("units") == "mm"
        assert ds["TOTAL_PRECIPITATION"].min() >= 0
        assert ds["TOTAL_PRECIPITATION"].max() < 500
    if "MAX_REL_HUMIDITY" in ds:
        # Humidity is usually in percent, but could be unitless
        units = ds["MAX_REL_HUMIDITY"].attrs.get("units")
        assert units in ("%", None, "")
        assert ds["MAX_REL_HUMIDITY"].min() >= 0
        assert ds["MAX_REL_HUMIDITY"].max() <= 100
    if "MEAN_PRESSURE" in ds:
        assert ds["MEAN_PRESSURE"].attrs.get("units") == "kPa"
        assert ds["MEAN_PRESSURE"].min() > 85
        assert ds["MEAN_PRESSURE"].max() < 110
    if "MEAN_WIND_SPEED" in ds:
        assert ds["MEAN_WIND_SPEED"].attrs.get("units") == "km/h"
        assert ds["MEAN_WIND_SPEED"].min() >= 0
        assert ds["MEAN_WIND_SPEED"].max() < 200

def test_hydrometric_units_and_ranges():
    station = "02GA018"
    ha = HydrometricStations(stn_id=station, start_date=datetime(2020, 1, 1), end_date=datetime(2020, 1, 10))
    ds = ha.to_xr()
    if "DISCHARGE" in ds:
        assert ds["DISCHARGE"].attrs.get("units") == "m3 s-1"
        assert ds["DISCHARGE"].min() >= 0
        assert ds["DISCHARGE"].max() < 100000
    if "LEVEL" in ds:
        assert ds["LEVEL"].attrs.get("units") == "m"
        assert ds["LEVEL"].min() >= 0
        assert ds["LEVEL"].max() < 20
