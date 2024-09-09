from datetime import datetime
from typing import List, Optional, Union

from .base import GeoMetAPI
from .utils.handlers import WeatherStationsDataHandler

"""
https://api.weather.gc.ca/
https://api.weather.gc.ca/openapi?f=html
https://climate.weather.gc.ca/historical_data/search_historic_data_e.html
https://climatedata.ca/
https://eccc-msc.github.io/open-data/msc-data/readme_en/
https://eccc-msc.github.io/open-data/msc-geomet/ogc_api_en/
"""


class WeatherStations(GeoMetAPI):
    """Weather station class for retrieving data from the Government of Canada's historical weather data API.

    Attributes
    ----------
    stn_id : Union[str, List[str]]
        The station number(s) to retrieve data for. If `bbox` is not specified, `stn_id` must be specified.
    start_date : Optional[datetime]
        The start date of the data to retrieve. If not specified, the default is 1840, 3, 1.
    end_date : Optional[datetime]
        The end date of the data to retrieve. If not specified, the default is the current date at midnight.
    bbox : Optional[List[float]]
        The bounding box to retrieve data for (left, bottom, right, top).
        If `stn_id` is not specified, `bbox` must be specified.
    hourly : bool
        If True, retrieve the hourly-data. If False, retrieve daily data.
    vars : Optional[List[str]]
        The variables to retrieve. If not specified, all variables are retrieved.
    """

    def __init__(
        self,
        stn_id: Optional[Union[str, List[str]]] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        bbox: Optional[List[float]] = None,
        hourly: bool = False,
        vars: Optional[List[str]] = None,
    ):
        super().__init__(
            stn_id=stn_id,
            start_date=start_date,
            end_date=end_date,
            bbox=bbox,
            hourly=hourly,
            vars=vars,
            data_handler=WeatherStationsDataHandler,
        )
