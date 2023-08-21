from weather_api import WeatherStations

station_number = "3053600"

def test_get_url():
    weather_stations = WeatherStations(stn_id=station_number)
    url = weather_stations.get_url()
    assert isinstance(url[0], str)