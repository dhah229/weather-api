from datetime import datetime

import folium
import pandas as pd
import xarray as xr

from weather_api import HydrometricStations, WeatherStations
from weather_api.base import GeoMetAPI

start_date = datetime(2020, 1, 1)
end_date = datetime(2020, 3, 1)
hydrometric_station = "02GA018"
weather_station = "6158355"
bbox = [-79.8, 43.63, -79.0, 43.9]
hydrometric_variables = "DISCHARGE"
weather_variables = "MEAN_TEMPERATURE"


def url(accessor: GeoMetAPI, station: str):
    wa: GeoMetAPI = accessor(stn_id=station, start_date=start_date, end_date=end_date)
    url = wa.get_url()
    assert isinstance(url[0], str)


def metadata(accessor: GeoMetAPI, station: str):
    wa: GeoMetAPI = accessor(stn_id=station)
    metadata = wa.get_metadata()
    assert isinstance(metadata, pd.DataFrame)
    wa: GeoMetAPI = accessor(stn_id=[station])
    metadata = wa.get_metadata()
    assert isinstance(metadata, pd.DataFrame)


def dataframe(accessor: GeoMetAPI, station: str):
    wa: GeoMetAPI = accessor(stn_id=station, start_date=start_date, end_date=end_date)
    dcf = wa.to_dict_frame()
    assert isinstance(dcf[station], pd.DataFrame)


def xarray(accessor: GeoMetAPI, station: str):
    wa: GeoMetAPI = accessor(stn_id=station, start_date=start_date, end_date=end_date)
    ds = wa.to_xr()
    assert isinstance(ds, xr.Dataset)


def plot_stations(accessor: GeoMetAPI, station: str):
    wa: GeoMetAPI = accessor(stn_id=station)
    m = wa.plot_stations()
    assert isinstance(m, folium.Map)


def bbox_url(accessor: GeoMetAPI):
    wa: GeoMetAPI = accessor(bbox=bbox)
    urls = wa.url
    assert isinstance(urls[0], str)


def variables(accessor: GeoMetAPI, station: str, vars: str):
    wa: GeoMetAPI = accessor(
        stn_id=station, vars=vars, start_date=start_date, end_date=end_date
    )
    ds = wa.to_xr()
    assert isinstance(ds, xr.Dataset)


def test_weather_url():
    url(accessor=WeatherStations, station=weather_station)


def test_hydrometric_url():
    url(accessor=HydrometricStations, station=hydrometric_station)


def test_weather_metadata():
    metadata(accessor=WeatherStations, station=weather_station)


def test_hydrometric_metadata():
    metadata(accessor=HydrometricStations, station=hydrometric_station)


def test_weather_dataframe():
    dataframe(accessor=WeatherStations, station=weather_station)


def test_hydrometric_dataframe():
    dataframe(accessor=HydrometricStations, station=hydrometric_station)


def test_weather_xarray():
    xarray(accessor=WeatherStations, station=weather_station)


def test_hydrometric_xarray():
    xarray(accessor=HydrometricStations, station=hydrometric_station)


def test_hydrometric_realtime():
    wa = HydrometricStations(stn_id=hydrometric_station, realtime=True)
    ds = wa.to_xr()
    assert isinstance(ds, xr.Dataset)


def test_weather_hourly():
    wa = WeatherStations(
        stn_id=weather_station,
        hourly=True,
        start_date=start_date,
        end_date=end_date,
    )
    ds = wa.to_xr()
    assert isinstance(ds, xr.Dataset)


def test_weather_plot_stations():
    plot_stations(accessor=WeatherStations, station=weather_station)


def test_hydrometric_plot_stations():
    plot_stations(accessor=HydrometricStations, station=hydrometric_station)


def test_bbox_url_weather():
    bbox_url(accessor=WeatherStations)


def test_bbox_url_hydrometric():
    bbox_url(accessor=HydrometricStations)


def test_variables_weather():
    variables(
        accessor=WeatherStations,
        station=weather_station,
        vars=weather_variables,
    )


def test_variables_hydrometric():
    variables(
        accessor=HydrometricStations,
        station=hydrometric_station,
        vars=hydrometric_variables,
    )


def test_variables_not_allowed_weather():
    try:
        variables(
            accessor=WeatherStations,
            station=weather_station,
            vars="not_allowed",
        )
    except ValueError:
        pass
    else:
        assert False, "Should have raised a ValueError"


def test_variables_not_allowed_hydrometric():
    try:
        variables(
            accessor=HydrometricStations,
            station=hydrometric_station,
            vars="not_allowed",
        )
    except ValueError:
        pass
    else:
        assert False, "Should have raised a ValueError"


def test_variables_not_allowed_weather_hourly():
    try:
        WeatherStations(
            stn_id=weather_station,
            hourly=True,
            vars="not_allowed",
        )
    except ValueError:
        pass
    else:
        assert False, "Should have raised a ValueError"


def test_variables_not_allowed_hydrometric_realtime():
    try:
        HydrometricStations(
            stn_id=hydrometric_station,
            realtime=True,
            vars="not_allowed",
        )
    except ValueError:
        pass
    else:
        assert False, "Should have raised a ValueError"
