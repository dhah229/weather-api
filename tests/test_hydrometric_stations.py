from weather_api import HydrometricStations

station_number = "05MH001"

def test_get_url():
    hydrometric_stations = HydrometricStations(stn_id=station_number)
    url = hydrometric_stations.get_url()
    assert isinstance(url[0], str)