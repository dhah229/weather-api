from datetime import datetime
import pandas as pd
from typing import Union, Optional, Dict
import folium
import xarray as xr
from .utils.dataframe import WeatherStationsDataframe
from .utils.url_handler import WeatherStationsUrlHandler
from .utils.xarray import WeatherStationsXArray
from .utils.plot_map import plot_weather_stations


"""
https://api.weather.gc.ca/
https://api.weather.gc.ca/openapi?f=html
https://climate.weather.gc.ca/historical_data/search_historic_data_e.html
https://climatedata.ca/
"""


class WeatherStations:
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
        self.stn_id = stn_id
        self.bbox = bbox
        if start_date is None:
            self.start_date = datetime(1840, 3, 1)
        else:
            self.start_date = start_date
        if end_date is None:
            end_date = datetime.now()
            self.end_date = end_date.replace(hour=0, minute=0, second=0)
        else:
            self.end_date = end_date
        self.url_handler = WeatherStationsUrlHandler(
            self.start_date, self.end_date, self.stn_id, self.bbox
        )
        self.url = self.get_url()
        self.dict_frame = None
        self.ds = None

    def get_url(self) -> str:
        """Build the URL to retrieve the data from."""
        url = self.url_handler.build_url()
        return url

    def get_metadata(self) -> pd.DataFrame:
        """Retrieve the metadata for the specified station(s)."""
        metadata_url = self.url_handler.build_url_metadata()
        dfs = [pd.read_csv(url) for url in metadata_url]
        df = pd.concat(dfs)
        return df

    def to_dict_frame(self) -> Dict[str, pd.DataFrame]:
        """Retrieve the data to a dictionary of pandas dataframes."""
        data_handler = WeatherStationsDataframe(self.url)
        self.dict_frame = data_handler.to_dict_frame()
        return self.dict_frame

    def to_xr(self) -> xr.Dataset:
        """Retrieve the data to an xarray dataset."""
        if self.dict_frame is None:
            self.dict_frame = self.to_dict_frame()
        data_handler = WeatherStationsXArray(self.dict_frame)
        ds = data_handler.to_xr()
        return ds

    def plot_stations(
        self, meta: Union[None, pd.DataFrame] = None,
    ) -> folium.Map:
        """Plot the weather stations on a map.

        If `meta` is not specified, the default metadata will be retrieved. It is recommended to use this with
        Jupyter Notebook to display the map.
        """
        if meta is None:
            meta = self.get_metadata()
        m = plot_weather_stations(meta)
        return m
