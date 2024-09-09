from datetime import datetime

from weather_api.utils.url_builder import UrlBuilder

route = "climate-daily"
start_date = datetime(2019, 1, 1)
end_date = datetime(2019, 2, 1)


def test_date_range():
    ub = UrlBuilder(route=route)
    ub.date_range = (start_date, end_date)
    assert ub.date_range == "2019-01-01 00:00:00/2019-02-01 00:00:00"
