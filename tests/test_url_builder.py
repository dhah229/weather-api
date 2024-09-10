from datetime import datetime

from weather_api.utils.url_builder import UrlBuilder

route = "climate-daily"
start_date = datetime(2019, 1, 1)
end_date = datetime(2019, 2, 1)


def test_date_range():
    ub = UrlBuilder(route=route)
    ub.date_range = (start_date, end_date)
    assert ub.date_range == "2019-01-01 00:00:00/2019-02-01 00:00:00"


def test_setter_getter():
    ub = UrlBuilder(route=route)
    ub.date_range_hydrometric = (start_date, end_date)
    assert ub.date_range_hydrometric == "2019-01-01/2019-02-01"

    ub.sortby = "DATE"
    assert ub.sortby == "DATE"

    ub.format = "csv"
    assert ub.format == "csv"

    ub.limit = 10
    assert ub.limit == 10

    ub.startindex = 10
    assert ub.startindex == 10

    ub.bbox = [1, 1, 1, 1]
    assert ub.bbox == "1,1,1,1"

    ub.climate_identifier = 1
    assert ub.climate_identifier == 1

    ub.station_number = "TEST1234"
    assert ub.station_number == "TEST1234"

    ub.properties = ["DISCHARGE", "LEVEL"]
    assert ub.properties == "DISCHARGE,LEVEL"
