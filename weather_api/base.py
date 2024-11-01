from abc import ABC
from datetime import datetime
from typing import Dict, List, Optional, Union

import folium
import pandas as pd
import xarray as xr

from .utils.dataframe import (
    DataFrameHandler,
    HydrometricStationsDataframe,
    WeatherStationsDataframe,
)
from .utils.handlers import DataHandler
from .utils.url_handler import (
    HydrometricStationsUrlHandler,
    UrlHandler,
    WeatherStationsUrlHandler,
)
from .utils.xarray import XArrayHandler


class GeoMetAPI(ABC):

    def __init__(
        self,
        stn_id: Union[str, List[str]],
        start_date: Optional[datetime],
        end_date: Optional[datetime],
        bbox: Optional[List[float]],
        data_handler: DataHandler,
        realtime: bool = False,  # for HydrometricStations
        hourly: bool = False,  # for WeatherStations
        vars: Optional[List[str]] = None,
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

        self.realtime = realtime
        self.hourly = hourly
        self.vars = vars
        self._initialize_url_handler(data_handler.url_handler)
        self.url = self.get_url()
        self.dataframe_handler = data_handler.dataframe_handler
        self.xarray_handler = data_handler.xarray_handler
        self.plotting_handler = data_handler.plotting_handler
        self.dict_frame = None
        self.ds = None

    def _initialize_url_handler(self, url_handler: UrlHandler):
        kwargs = {
            "start_date": self.start_date,
            "end_date": self.end_date,
            "stn_id": self.stn_id,
            "bbox": self.bbox,
            "properties": self.vars,
        }
        if issubclass(url_handler, HydrometricStationsUrlHandler):
            kwargs["realtime"] = self.realtime
        if issubclass(url_handler, WeatherStationsUrlHandler):
            kwargs["hourly"] = self.hourly
        self.url_handler: UrlHandler = url_handler(**kwargs)

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
        kwargs = {}
        if issubclass(self.dataframe_handler, HydrometricStationsDataframe):
            kwargs = {"realtime": self.realtime}
        elif issubclass(self.dataframe_handler, WeatherStationsDataframe):
            kwargs = {"hourly": self.hourly}
        data_handler: DataFrameHandler = self.dataframe_handler(self.url, **kwargs)
        self.dict_frame = data_handler.to_dict_frame()
        return self.dict_frame

    def to_xr(self) -> xr.Dataset:
        """Retrieve the data to an xarray dataset."""
        if self.dict_frame is None:
            self.dict_frame = self.to_dict_frame()
        data_handler: XArrayHandler = self.xarray_handler(self.dict_frame)
        ds = data_handler.to_xr()
        return ds

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
        m = self.plotting_handler.plot_stations(meta)
        return m
