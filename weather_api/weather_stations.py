from datetime import datetime
from typing import Optional, Union

import folium
import pandas as pd

from .base import GeoMetAPI
from .utils.dataframe import WeatherStationsDataframe
from .utils.plot_map import plot_weather_stations
from .utils.url_handler import WeatherStationsUrlHandler
from .utils.xarray import WeatherStationsXArray

"""
https://api.weather.gc.ca/
https://api.weather.gc.ca/openapi?f=html
https://climate.weather.gc.ca/historical_data/search_historic_data_e.html
https://climatedata.ca/
"""


class WeatherStations(GeoMetAPI):
    """Weather station class for retrieving data from the Government of Canada's historical weather data API.

    Attributes
    ----------
    stn_id : Union[str, list]
        The station number(s) to retrieve data for. If `bbox` is not specified, `stn_id` must be specified.
    start_date : Optional[datetime]
        The start date of the data to retrieve. If not specified, the default is 1840, 3, 1.
    end_date : Optional[datetime]
        The end date of the data to retrieve. If not specified, the default is the current date at midnight.
    bbox : Optional[list]
        The bounding box to retrieve data for (left, bottom, right, top).
        If `stn_id` is not specified, `bbox` must be specified.
    """

    def __init__(
        self,
        stn_id: Union[str, list] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        bbox: Optional[list] = None,
    ):
        super().__init__(
            stn_id=stn_id,
            start_date=start_date,
            end_date=end_date,
            bbox=bbox,
            url_handler=WeatherStationsUrlHandler,
            dataframe_handler=WeatherStationsDataframe,
            xarray_handler=WeatherStationsXArray,
        )

    def plot_stations(
        self,
        meta: Union[None, pd.DataFrame] = None,
    ) -> folium.Map:
        """Plot the weather stations on a map.

        If `meta` is not specified, the default metadata will be retrieved. It is recommended to use this with
        Jupyter Notebook to display the map.
        """
        if meta is None:
            meta = self.get_metadata()
        m = plot_weather_stations(meta)
        return m
