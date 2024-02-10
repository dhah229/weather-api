from weather_api import HydrometricStations
import pandas as pd
import xarray as xr

station_number = "02GA018"

def test_get_url():
    hydrometric_stations = HydrometricStations(stn_id=station_number)
    url = hydrometric_stations.get_url()
    assert isinstance(url[0], str)

def test_get_metadata():
    hydrometric_stations = HydrometricStations(stn_id=station_number)
    metadata = hydrometric_stations.get_metadata()
    assert isinstance(metadata, pd.DataFrame)

def test_get_dataframe():
    hydrometric_stations = HydrometricStations(stn_id=station_number)
    df = hydrometric_stations.to_dict_frame()
    assert isinstance(df, dict)
    assert isinstance(df[station_number], pd.DataFrame)

def test_get_xr():
    hydrometric_stations = HydrometricStations(stn_id=station_number)
    ds = hydrometric_stations.to_xr()
    assert isinstance(ds, xr.Dataset)
